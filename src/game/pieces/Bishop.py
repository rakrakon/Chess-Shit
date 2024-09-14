from typing import List, Optional

from src.game.Constants import BOARD_SIZE
from src.game.pieces.Piece import Piece


class Bishop(Piece):
    def get_valid_moves(self, board: List[List[Optional[Piece]]], position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []
        x, y = position

        # Up-left
        for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            if board[i][j] is None:
                valid_moves.append((i, j))
            elif board[i][j].color != self.color:
                valid_moves.append((i, j))
                break
            else:
                break

        # Up-right
        for i, j in zip(range(x - 1, -1, -1), range(y + 1, BOARD_SIZE)):
            if board[i][j] is None:
                valid_moves.append((i, j))
            elif board[i][j].color != self.color:
                valid_moves.append((i, j))
                break
            else:
                break

        # Down-left
        for i, j in zip(range(x + 1, BOARD_SIZE), range(y - 1, -1, -1)):
            if board[i][j] is None:
                valid_moves.append((i, j))
            elif board[i][j].color != self.color:
                valid_moves.append((i, j))
                break
            else:
                break

        # Down-right
        for i, j in zip(range(x + 1, BOARD_SIZE), range(y + 1, BOARD_SIZE)):
            if board[i][j] is None:
                valid_moves.append((i, j))
            elif board[i][j].color != self.color:
                valid_moves.append((i, j))
                break
            else:
                break

        return valid_moves
