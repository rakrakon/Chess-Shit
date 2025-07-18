from typing import List, Tuple
from src.game.Aliases import TBoard
from src.game.pieces.Piece import Piece


def is_clear_path(board: TBoard, start, end, y):
    step = 1 if start < end else -1
    for x in range(start + step, end, step):
        if board[y][x] is not None:
            return False
    return True


class King(Piece):
    def get_valid_moves(self, board: TBoard, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        valid_moves = self.get_basic_moves(board, position)
        valid_moves.extend(self.get_castling_moves(board, position))
        return valid_moves

    def move(self, board: 'Board', from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if abs(to_col - from_col) == 2:
            rook_from_col = 7 if to_col > from_col else 0
            rook_to_col = (from_col + to_col) // 2

            rook = board.get_piece((from_row, rook_from_col))
            rook.move(board, (from_row, rook_from_col), (to_row, rook_to_col))

        super().move(board, from_pos, to_pos)

    def get_basic_moves(self, board: TBoard, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = position
        king_moves = [
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
        ]

        return [
            move for move in king_moves
            if self.is_valid_move(board, move)
        ]

    def is_valid_move(self, board: TBoard, move: Tuple[int, int]) -> bool:
        new_x, new_y = move
        board_length = len(board)
        if 0 <= new_x < board_length and 0 <= new_y < board_length:
            return board[new_y][new_x] is None or board[new_y][new_x].color != self.color
        return False

    def get_castling_moves(self, board: TBoard, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        castling_moves = []
        x, y = position

        if not self.has_moved:
            if self.check_rook_movement(board, 7) and is_clear_path(board, x + 1, 7, y):  # Kingside
                castling_moves.append((x + 2, y))
            if self.check_rook_movement(board, 0) and is_clear_path(board, x - 1, 0, y):  # Queenside
                castling_moves.append((x - 2, y))

        return castling_moves

    def check_rook_movement(self, board: TBoard, rook_file: int) -> bool:
        return not board[self.color.starting_row - self.color.direction][rook_file].has_moved
