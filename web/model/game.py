from uuid import UUID

from web.model.game_field import GameField


class Game:
    def __init__(self, game_id: UUID, field: GameField):
        self.game_id = game_id
        self.field = field

    def to_dict(self) -> dict:
        return {
            "id": str(self.game_id),
            "field": self.field.cells,
        }