from domain.service.game_rules import (
    COMPUTER,
    EMPTY,
    PLAYER,
    get_winner,
    is_full,
)


def get_best_move(cells: list[list[int]]) -> tuple[int, int] | None:
    best_score = float("-inf")
    best_move = None

    for row in range(3):
        for column in range(3):
            if cells[row][column] == EMPTY:
                cells[row][column] = COMPUTER

                score = _minimax(
                    cells,
                    is_maximizing=False,
                    depth=0,
                )

                cells[row][column] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (row, column)

    return best_move


def _minimax(
    cells: list[list[int]],
    is_maximizing: bool,
    depth: int,
) -> int:
    winner = get_winner(cells)

    if winner == COMPUTER:
        return 10 - depth

    if winner == PLAYER:
        return depth - 10

    if is_full(cells):
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for row in range(3):
            for column in range(3):
                if cells[row][column] == EMPTY:
                    cells[row][column] = COMPUTER

                    score = _minimax(
                        cells,
                        False,
                        depth + 1,
                    )

                    cells[row][column] = EMPTY

                    best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for row in range(3):
        for column in range(3):
            if cells[row][column] == EMPTY:
                cells[row][column] = PLAYER

                score = _minimax(
                    cells,
                    True,
                    depth + 1,
                )

                cells[row][column] = EMPTY

                best_score = min(best_score, score)

    return best_score