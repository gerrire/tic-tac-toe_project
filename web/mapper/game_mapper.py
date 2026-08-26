from copy import deepcopy

from domain.model.game import Game as DomainGame
from domain.model.game_field import GameField as DomainGameField
from web.model.game import Game as WebGame
from web.model.game_field import GameField as WebGameField


def web_to_domain(game: WebGame) -> DomainGame:
    return DomainGame(
        game_id=game.game_id,
        field=DomainGameField(
            cells=deepcopy(game.field.cells)
        ),
    )


def domain_to_web(game: DomainGame) -> WebGame:
    return WebGame(
        game_id=game.game_id,
        field=WebGameField(
            cells=deepcopy(game.field.cells)
        ),
    )