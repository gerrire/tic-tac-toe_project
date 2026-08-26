EMPTY = 0
PLAYER = 1
COMPUTER = 2


def get_winner(cells: list[list[int]]) -> int | None:
    lines = []

    lines.extend(cells)

    for column in range(3):
        lines.append([
            cells[0][column],
            cells[1][column],
            cells[2][column],
        ])

    lines.append([
        cells[0][0],
        cells[1][1],
        cells[2][2],
    ])

    lines.append([
        cells[0][2],
        cells[1][1],
        cells[2][0],
    ])

    for line in lines:
        if line == [PLAYER, PLAYER, PLAYER]:
            return PLAYER

        if line == [COMPUTER, COMPUTER, COMPUTER]:
            return COMPUTER

    return None


def is_full(cells: list[list[int]]) -> bool:
    for row in cells:
        if EMPTY in row:
            return False

    return True