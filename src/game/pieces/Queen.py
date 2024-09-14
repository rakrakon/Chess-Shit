from typing import List, Optional

from src.game.pieces.Bishop import Bishop
from src.game.pieces.Piece import Piece
from src.game.pieces.Rook import Rook


class Queen(Piece):
    def get_valid_moves(self, board: List[List[Optional[Piece]]], position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []

        rook = Rook(self.color)
        bishop = Bishop(self.color)

        valid_moves += rook.get_valid_moves(board, position)
        valid_moves += bishop.get_valid_moves(board, position)

        return valid_moves
