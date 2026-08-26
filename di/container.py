from datasource.repository.game_repository_impl import GameRepositoryImpl
from datasource.repository.game_storage import GameStorage
from domain.service.game_service_impl import GameServiceImpl
from web.module.game_module import create_game_module


class Container:
    def __init__(self):
        self.game_storage = GameStorage()

        self.game_repository = GameRepositoryImpl(
            self.game_storage
        )

        self.game_service = GameServiceImpl(
            self.game_repository
        )

        self.game_module = create_game_module(
            self.game_service
        )