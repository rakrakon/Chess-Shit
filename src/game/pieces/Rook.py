from typing import List

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.pieces.King import King
from src.game.pieces.Piece import Piece, adjust_for_checking


class Rook(Piece):
    def update_is_checking(self, piece):
        if isinstance(piece, King):
            self.is_checking = True

    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        self.is_checking = False
        valid_moves: List[tuple[int, int]] = []

        row, col = position

        # Vertical Down
        for r in range(row + 1, BOARD_SIZE):
            if board[r][col] is None:
                valid_moves.append((r, col))
            elif board[r][col].color != self.color:
                self.update_is_checking(board[r][col])
                valid_moves.append((r, col))
                break
            else:
                break

        # Vertical Up
        for r in range(row - 1, -1, -1):
            if board[r][col] is None:
                valid_moves.append((r, col))
            elif board[r][col].color != self.color:
                self.update_is_checking(board[r][col])
                valid_moves.append((r, col))
                break
            else:
                break

        # Horizontal Right
        for c in range(col + 1, BOARD_SIZE):
            if board[row][c] is None:
                valid_moves.append((row, c))
            elif board[row][c].color != self.color:
                self.update_is_checking(board[row][c])
                valid_moves.append((row, c))
                break
            else:
                break

        # Horizontal Left
        for c in range(col - 1, -1, -1):
            if board[row][c] is None:
                valid_moves.append((row, c))
            elif board[row][c].color != self.color:
                self.update_is_checking(board[row][c])
                valid_moves.append((row, c))
                break
            else:
                break

        return adjust_for_checking(self.color, position, board, valid_moves)