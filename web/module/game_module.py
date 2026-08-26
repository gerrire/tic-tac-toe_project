from flask import Blueprint

from domain.service.game_service import GameService
from web.route.game_route import register_game_routes
from web.route.page_route import register_page_routes


def create_game_module(
    game_service: GameService,
) -> Blueprint:
    blueprint = Blueprint(
        "game",
        __name__,
    )

    register_page_routes(blueprint)

    register_game_routes(
        blueprint,
        game_service,
    )

    return blueprint