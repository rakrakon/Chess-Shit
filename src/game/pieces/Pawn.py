from typing import List, Optional

from src.game.pieces.Piece import Piece


class Pawn(Piece):
    def get_valid_moves(self, board, position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []

        x, y = position
        forward_step = y + self.color.direction
        double_forward_step = y + self.color.direction * 2

        if 0 <= forward_step < len(board):
            if board[forward_step][x] is None:
                valid_moves.append((x, forward_step))

                if y == self.color.starting_row and board[double_forward_step][x] is None:
                    valid_moves.append((x, double_forward_step))

            if x + 1 < len(board[0]) and board[forward_step][x + 1] and board[forward_step][x + 1].color != self.color:
                valid_moves.append((x + 1, forward_step))

            if x - 1 >= 0 and board[forward_step][x - 1] and board[forward_step][x - 1].color != self.color:
                valid_moves.append((x - 1, forward_step))

        return valid_moves
