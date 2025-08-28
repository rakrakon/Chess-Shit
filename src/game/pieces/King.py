from typing import List, Tuple
from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.pieces.Piece import Piece


def is_clear_path(board: TBoard, start, end, y):
    step = 1 if start < end else -1
    for x in range(start + step, end, step):
        if board[y][x] is not None:
            return False
    return True


def get_king_moves(position):
    x, y = position
    return [
        (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
        (x, y - 1), (x, y + 1),
        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
    ]


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
        king_moves = get_king_moves(position)

        return [
            move for move in king_moves
            if self.is_valid_move(board, move) and not self.is_enemy_king_present(move, board) and move not in self.get_all_threatened_grids(board)
        ]

    def is_enemy_king_present(self, position, board):
        moves = get_king_moves(position)
        for move in moves:
            nx, ny = move
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                piece = board[ny][nx]
                if isinstance(piece, King) and piece.color != self.color:
                    return True
        return False

    def get_all_threatened_grids(self, board: TBoard):
        grids = []
        for row_idx, row in enumerate(board):
            for col_idx, piece in enumerate(row):
                if piece is None or piece.color == self.color or isinstance(piece, King):
                    continue

                if piece.__str__() == "P": # Pawn Piece
                    forward_row = row_idx + piece.color.direction
                    grids += [(col_idx + 1, forward_row), (col_idx - 1, forward_row)]
                    continue

                grids += piece.get_valid_moves(board, (col_idx, row_idx))
        return grids

    def is_valid_move(self, board: TBoard, move: Tuple[int, int]) -> bool:
        new_x, new_y = move
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            return board[new_x][new_y] is None or board[new_x][new_y].color != self.color
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
        rook_location = board[self.color.starting_row - self.color.direction][rook_file]
        return rook_location.__str__() == "R" and not rook_location.has_moved # Rook Piece
