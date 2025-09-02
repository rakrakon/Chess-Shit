from typing import List, Tuple

import copy
from src.game.Color import Color
from src.game.Constants import BOARD_SIZE


def is_any_piece_checking_color(board, color):
    for row in board:
        for piece in row:
            if piece is None:
                continue

            if piece.color != color and piece.is_checking:
                return True
    return False


def adjust_for_checking(color, position, board, valid_moves):
    adjusted_valid_moves = []
    for move in valid_moves:
        testboard = copy.deepcopy(board)
        testboard[move[0]][move[1]] = testboard[position[0]][position[1]]
        testboard[position[0]][position[1]] = None
        if not is_any_piece_checking_color(testboard, color):
            adjusted_valid_moves.append(move)
    return adjusted_valid_moves


class Piece:

    def __init__(self, color: Color):
        self.color = color
        self.has_moved = False
        self.is_checking = False

    def get_valid_moves(self, board, position: tuple[int, int]) -> List[tuple[int, int]]:
        pass

    def move(self, board: 'Board', from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        self.has_moved = True
        board.set_piece(to_pos, self)
        board.set_piece(from_pos, None)

        pawn_two_step_row = self.color.opposite_row - 3 * self.color.direction
        for i in range(BOARD_SIZE):
            piece = board.get_piece((pawn_two_step_row, i))
            try:
                piece.has_two_stepped = False
            except:
                pass

    def __str__(self):
        return self.__class__.__name__[0]
