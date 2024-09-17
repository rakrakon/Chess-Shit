from typing import List, Optional, Tuple

from src.game.Aliases import TBoard
from src.game.pieces.Piece import Piece
from src.game.Constants import BOARD_SIZE


class Pawn(Piece):
    has_two_stepped = False

    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []

        x, y = position
        forward_step = y + self.color.direction
        double_forward_step = y + self.color.direction * 2

        if 0 <= forward_step < BOARD_SIZE:
            if board[forward_step][x] is None:
                valid_moves.append((x, forward_step))

                if y == self.color.starting_row and board[double_forward_step][x] is None:
                    valid_moves.append((x, double_forward_step))

            if x + 1 < len(board[0]) and board[forward_step][x + 1] and board[forward_step][x + 1].color != self.color:
                valid_moves.append((x + 1, forward_step))

            if x - 1 >= 0 and board[forward_step][x - 1] and board[forward_step][x - 1].color != self.color:
                valid_moves.append((x - 1, forward_step))

            if x != BOARD_SIZE - 1 and type(board[y][x + 1]) == Pawn and board[y][x + 1].has_two_stepped:
                valid_moves.append((x + 1, forward_step))

            if x != 0 and type(board[y][x - 1]) == Pawn and board[y][x - 1].has_two_stepped:
                valid_moves.append((x - 1, forward_step))

        return valid_moves

    def move(self, board: 'Board', from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        double_step = self.color.direction * 2
        if from_row == self.color.starting_row and to_row == from_row + double_step:
            self.has_two_stepped = True

        is_at_opponent_pawn_two_step = from_row == self.color.opposite_row  - 3 * self.color.direction
        is_moving_diagonally = abs(from_col - to_col) == 1

        if is_at_opponent_pawn_two_step and is_moving_diagonally and type(board.get_piece((from_row, to_col))) == Pawn:
            board.set_piece((from_row, to_col), None)

        super().move(board, from_pos, to_pos)

