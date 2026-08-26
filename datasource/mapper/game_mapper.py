from datasource.model.game import Game as DataGame
from datasource.model.game_field import GameField as DataGameField
from domain.model.game import Game as DomainGame
from domain.model.game_field import GameField as DomainGameField


def domain_to_data(game: DomainGame) -> DataGame:
    return DataGame(
        game_id=game.game_id,
        field=DataGameField(
            cells=[row.copy() for row in game.field.cells]
        ),
    )


def data_to_domain(game: DataGame) -> DomainGame:
    return DomainGame(
        game_id=game.game_id,
        field=DomainGameField(
            cells=[row.copy() for row in game.field.cells]
        ),
    )