from typing import List, Optional

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.pieces.King import King
from src.game.pieces.Piece import Piece


class Bishop(Piece):
    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        self.is_checking = False
        valid_moves: List[tuple[int, int]] = []
        row, col = position

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d_row, d_col in directions:
            n_row, n_col = row + d_row, col + d_col

            while 0 <= n_row < BOARD_SIZE and 0 <= n_col < BOARD_SIZE:
                if board[n_row][n_col] is None:
                    valid_moves.append((n_row, n_col))
                elif board[n_row][n_col].color != self.color:
                    if isinstance(board[n_row][n_col], King):
                        self.is_checking = True
                    valid_moves.append((n_row, n_col))
                    break
                else:
                    break

                n_row += d_row
                n_col += d_col

        return valid_moves
