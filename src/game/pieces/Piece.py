from typing import List, Optional

from src.game.Color import Color


class Piece:
    def __init__(self, color: Color):
        self.color = color

    def get_valid_moves(self, board, position: tuple[int, int]) -> List[tuple[int, int]]:
        pass

    def __str__(self):
        return self.__class__.__name__[0]
