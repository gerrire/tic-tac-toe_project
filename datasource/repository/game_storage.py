import json
import sqlite3

from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from threading import RLock
from uuid import UUID

from datasource.model.game import Game
from datasource.model.game_field import GameField


class GameStorage:
    CACHE_SIZE = 100

    def __init__(self, database_path: str = "data/games.db"):
        self._games: OrderedDict[UUID, Game] = OrderedDict()
        self._lock = RLock()

        self._database_path = Path(database_path)

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def save(self, game: Game) -> None:
        field_json = json.dumps(game.field.cells)

        with self._lock:
            connection = sqlite3.connect(
                self._database_path,
                timeout=5,
            )

            try:
                connection.execute(
                    """
                    INSERT INTO games (game_id, field)
                    VALUES (?, ?)
                    ON CONFLICT(game_id)
                    DO UPDATE SET
                        field = excluded.field
                    """,
                    (
                        str(game.game_id),
                        field_json,
                    ),
                )

                connection.commit()

            finally:
                connection.close()

            self._save_to_cache(game)

    def get(self, game_id: UUID) -> Game | None:
        with self._lock:
            cached_game = self._games.get(game_id)

            if cached_game is not None:
                self._games.move_to_end(game_id)

                return deepcopy(cached_game)

            connection = sqlite3.connect(
                self._database_path,
                timeout=5,
            )

            try:
                cursor = connection.execute(
                    """
                    SELECT field
                    FROM games
                    WHERE game_id = ?
                    """,
                    (str(game_id),),
                )

                row = cursor.fetchone()

            finally:
                connection.close()

            if row is None:
                return None

            cells = json.loads(row[0])

            game = Game(
                game_id=game_id,
                field=GameField(cells),
            )

            self._save_to_cache(game)

            return deepcopy(game)

    def _save_to_cache(self, game: Game) -> None:
        self._games[game.game_id] = deepcopy(game)

        self._games.move_to_end(game.game_id)

        if len(self._games) > self.CACHE_SIZE:
            self._games.popitem(last=False)

    def _initialize_database(self) -> None:
        connection = sqlite3.connect(
            self._database_path,
            timeout=5,
        )

        try:
            connection.execute(
                """
                PRAGMA journal_mode=WAL
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    field TEXT NOT NULL
                )
                """
            )

            connection.commit()

        finally:
            connection.close()