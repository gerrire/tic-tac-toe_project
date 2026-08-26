from uuid import UUID

from datasource.mapper.game_mapper import data_to_domain, domain_to_data
from datasource.repository.game_storage import GameStorage
from domain.model.game import Game
from domain.repository.game_repository import GameRepository


class GameRepositoryImpl(GameRepository):
    def __init__(self, storage: GameStorage):
        self._storage = storage

    def save(self, game: Game) -> None:
        data_game = domain_to_data(game)
        self._storage.save(data_game)

    def get(self, game_id: UUID) -> Game | None:
        data_game = self._storage.get(game_id)

        if data_game is None:
            return None

        return data_to_domain(data_game)