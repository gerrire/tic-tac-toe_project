from uuid import UUID

from flask import Blueprint, jsonify, request

from domain.exception.invalid_game_error import InvalidGameError
from domain.service.game_service import GameService
from web.mapper.game_mapper import domain_to_web, web_to_domain
from web.model.error_response import ErrorResponse
from web.model.game import Game
from web.model.game_field import GameField


def register_game_routes(
    blueprint: Blueprint,
    game_service: GameService,
) -> None:

    @blueprint.post("/game/<uuid:game_id>")
    def play_turn(game_id: UUID):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return _error("Request body must be valid JSON")

        if "id" not in data:
            return _error("Field 'id' is required")

        if "field" not in data:
            return _error("Field 'field' is required")

        try:
            body_game_id = UUID(str(data["id"]))
        except (ValueError, TypeError, AttributeError):
            return _error("Invalid game UUID")

        if body_game_id != game_id:
            return _error(
                "Game UUID in URL and request body must match"
            )

        web_game = Game(
            game_id=body_game_id,
            field=GameField(
                cells=data["field"]
            ),
        )

        try:
            domain_game = web_to_domain(web_game)
            updated_game = game_service.process_turn(domain_game)
        except InvalidGameError as error:
            return _error(str(error))

        response_game = domain_to_web(updated_game)

        return jsonify(response_game.to_dict()), 200


def _error(message: str):
    error = ErrorResponse(message)

    return jsonify(error.to_dict()), 400