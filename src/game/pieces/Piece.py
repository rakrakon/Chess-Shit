from typing import List, Tuple

from src.game.Color import Color


class Piece:

    def __init__(self, color: Color):
        self.color = color
        self.has_moved = False

    def get_valid_moves(self, board, position: tuple[int, int]) -> List[tuple[int, int]]:
        pass

    def move(self, board: 'Board', from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        self.has_moved = True
        board.set_piece(to_pos, self)
        board.set_piece(from_pos, None)

    def __str__(self):
        return self.__class__.__name__[0]
