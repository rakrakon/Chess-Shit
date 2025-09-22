from typing import List

from src.game.Aliases import TBoard
from src.game.pieces.King import King
from src.game.pieces.Piece import Piece


class Knight(Piece):
    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        self.is_checking = False
        valid_moves: List[tuple[int, int]] = []
        row, col = position
        knight_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1)
        ]

        for move in knight_moves:
            new_row, new_col = move
            board_length = len(board)
            if 0 <= new_row < board_length and 0 <= new_col < board_length:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    if isinstance(board[new_row][new_col], King):
                        self.is_checking = True
                    valid_moves.append(move)

        return valid_moves

    def __str__(self):
        return "KN"

