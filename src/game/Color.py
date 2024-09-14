from enum import Enum


class Color(Enum):
    WHITE = (-1, 7, 6)   # direction, opposite color's row, pawn's starting row
    BLACK = (1, 0, 1)  # direction, opposite color's row, pawn's starting row

    def __init__(self, direction: int, opposite_row: int, starting_row: int):
        self._direction = direction
        self._opposite_row = opposite_row
        self._starting_row = starting_row

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def opposite_row(self) -> int:
        return self._opposite_row

    @property
    def starting_row(self) -> int:
        return self._starting_row
