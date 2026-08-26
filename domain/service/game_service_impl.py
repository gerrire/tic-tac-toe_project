from copy import deepcopy

from domain.exception.invalid_game_error import InvalidGameError
from domain.model.game import Game
from domain.model.game_field import GameField
from domain.repository.game_repository import GameRepository
from domain.service.game_rules import (
    COMPUTER,
    EMPTY,
    PLAYER,
    get_winner,
    is_full,
)
from domain.service.game_service import GameService
from domain.service.minimax import get_best_move


class GameServiceImpl(GameService):
    def __init__(self, repository: GameRepository):
        self._repository = repository

    def get_next_move(self, game: Game) -> Game:
        cells = deepcopy(game.field.cells)

        move = get_best_move(cells)

        if move is None:
            return game

        row, column = move
        cells[row][column] = COMPUTER

        return Game(
            game.game_id,
            GameField(cells),
        )

    def validate_game(
        self,
        old_game: Game,
        new_game: Game,
    ) -> None:
        self._validate_field(new_game.field.cells)

        if old_game.game_id != new_game.game_id:
            raise InvalidGameError("Game UUID cannot be changed")

        if self.is_game_finished(old_game):
            raise InvalidGameError("Game is already finished")

        old_cells = old_game.field.cells
        new_cells = new_game.field.cells

        new_player_moves = 0

        for row in range(3):
            for column in range(3):
                old_cell = old_cells[row][column]
                new_cell = new_cells[row][column]

                if old_cell != EMPTY and old_cell != new_cell:
                    raise InvalidGameError(
                        "Previous moves cannot be changed"
                    )

                if old_cell == EMPTY and new_cell == COMPUTER:
                    raise InvalidGameError(
                        "Player cannot make computer moves"
                    )

                if old_cell == EMPTY and new_cell == PLAYER:
                    new_player_moves += 1

        if new_player_moves != 1:
            raise InvalidGameError(
                "Player must make exactly one move"
            )

    def is_game_finished(self, game: Game) -> bool:
        cells = game.field.cells

        return get_winner(cells) is not None or is_full(cells)

    def process_turn(self, game: Game) -> Game:
        old_game = self._repository.get(game.game_id)

        if old_game is None:
            old_game = Game(
                game.game_id,
                GameField([
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ]),
            )

        self.validate_game(old_game, game)

        if self.is_game_finished(game):
            self._repository.save(game)
            return game

        updated_game = self.get_next_move(game)

        self._repository.save(updated_game)

        return updated_game

    @staticmethod
    def _validate_field(cells: list[list[int]]) -> None:
        if not isinstance(cells, list) or len(cells) != 3:
            raise InvalidGameError(
                "Game field must contain exactly 3 rows"
            )

        for row in cells:
            if not isinstance(row, list) or len(row) != 3:
                raise InvalidGameError(
                    "Each game field row must contain exactly 3 cells"
                )

            for cell in row:
                if type(cell) is not int or cell not in (0, 1, 2):
                    raise InvalidGameError(
                        "Game field can contain only 0, 1 and 2"
                    )