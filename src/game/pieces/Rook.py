from typing import List, Optional

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.pieces.Piece import Piece


class Rook(Piece):
    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []

        x, y = position

        # Horizontal Right
        for i in range(x + 1, BOARD_SIZE):
            if board[y][i] is None:
                valid_moves.append((i, y))
            elif board[y][i].color != self.color:
                valid_moves.append((i, y))
                break
            else:
                break

        # Horizontal Left
        for i in range(x - 1, 0, -1):
            if board[y][i] is None:
                valid_moves.append((i, y))
            elif board[y][i].color != self.color:
                valid_moves.append((i, y))
                break
            else:
                break

        # Vertical Up
        for i in range(y + 1, BOARD_SIZE):
            if board[i][x] is None:
                valid_moves.append((x, i))
            elif board[i][x].color != self.color:
                valid_moves.append((x, i))
                break
            else:
                break

        # Vertical Down
        for i in range(y - 1, 0, -1):
            if board[i][x] is None:
                valid_moves.append((x, i))
            elif board[i][x].color != self.color:
                valid_moves.append((x, i))
                break
            else:
                break

        return valid_moves
