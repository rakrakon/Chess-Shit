from typing import List, Tuple

from src.game.Aliases import TBoard
from src.game.pieces.King import King
from src.game.pieces.Piece import Piece, adjust_for_checking
from src.game.Constants import BOARD_SIZE


class Pawn(Piece):
    has_two_stepped = False

    def update_is_checking(self, piece):
        if isinstance(piece, King):
            self.is_checking = True

    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        self.is_checking = False
        valid_moves: List[tuple[int, int]] = []

        row, col = position
        forward_step = row + self.color.direction
        double_forward_step = row + self.color.direction * 2

        if 0 <= forward_step < BOARD_SIZE:
            if board[forward_step][col] is None:
                self.update_is_checking(board[forward_step][col])
                valid_moves.append((forward_step, col))

                if row == self.color.starting_row and board[double_forward_step][col] is None:
                    self.update_is_checking(board[double_forward_step][col])
                    valid_moves.append((double_forward_step, col))

            if col + 1 < len(board[0]) and board[forward_step][col + 1] and board[forward_step][col + 1].color != self.color:
                self.update_is_checking(board[forward_step][col + 1])
                valid_moves.append((forward_step, col + 1))

            if col - 1 >= 0 and board[forward_step][col - 1] and board[forward_step][col - 1].color != self.color:
                self.update_is_checking(board[forward_step][col - 1])
                valid_moves.append((forward_step, col - 1))

            # Right side en passant
            if col != BOARD_SIZE - 1 and isinstance(board[row][col + 1], Pawn) and board[row][col + 1].has_two_stepped:
                self.update_is_checking(board[row][col + 1])
                valid_moves.append((forward_step, col + 1))

            # Left side en passant
            if col != 0 and isinstance(board[row][col - 1], Pawn) and board[row][col - 1].has_two_stepped:
                self.update_is_checking(board[row][col - 1])
                valid_moves.append((forward_step, col - 1))

        return adjust_for_checking(self.color, position, board, valid_moves)

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
