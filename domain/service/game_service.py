from abc import ABC, abstractmethod

from domain.model.game import Game


class GameService(ABC):
    @abstractmethod
    def get_next_move(self, game: Game) -> Game:
        pass

    @abstractmethod
    def validate_game(self, old_game: Game, new_game: Game) -> None:
        pass

    @abstractmethod
    def is_game_finished(self, game: Game) -> bool:
        pass

    @abstractmethod
    def process_turn(self, game: Game) -> Game:
        pass