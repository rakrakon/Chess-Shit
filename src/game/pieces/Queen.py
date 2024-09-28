from typing import List, Optional

from pygame.event import set_keyboard_grab

from src.game.Aliases import TBoard
from src.game.pieces.Bishop import Bishop
from src.game.pieces.Piece import Piece
from src.game.pieces.Rook import Rook


class Queen(Piece):
    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        self.is_checking = False
        valid_moves: List[tuple[int, int]] = []

        rook = Rook(self.color)
        bishop = Bishop(self.color)

        valid_moves += rook.get_valid_moves(board, position)
        valid_moves += bishop.get_valid_moves(board, position)

        self.is_checking = rook.is_checking or bishop.is_checking

        return valid_moves
