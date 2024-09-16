from typing import Tuple, List, Optional, TypeAlias

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.Color import Color
from src.game.pieces.Bishop import Bishop
from src.game.pieces.King import King
from src.game.pieces.Knight import Knight
from src.game.pieces.Pawn import Pawn
from src.game.pieces.Piece import Piece
from src.game.pieces.Queen import Queen
from src.game.pieces.Rook import Rook


class Board:

    def __init__(self):
        self.board: TBoard = create_initial_board()

    def print_board(self):
        for row in self.board:
            print(" | ".join([str(piece) if piece else " " for piece in row]))
            print("-" * 33)

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not is_valid_position(from_row, from_col):
            raise ValueError("Invalid source position")

        if not is_valid_position(to_row, to_col):
            raise ValueError("Invalid destination position")

        piece = self.board[from_row][from_col]

        if piece is None:
            raise ValueError("No piece at the source position")

        y, x = from_pos
        valid_moves = piece.get_valid_moves(self.board, (x, y))

        if (to_col, to_row) not in valid_moves:
            return False

        piece.has_moved = True

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        return True

    def get_piece(self, row: int, col: int) -> Piece:
        if not is_valid_position(row, col):
            raise ValueError("Invalid position")
        return self.board[row][col]

    def get_valid_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        row, col = position
        piece = self.get_piece(row, col)

        if piece is None:
            return []

        return piece.get_valid_moves(self.board, position)


def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def create_initial_board() -> TBoard:
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    setup_pieces(board)

    return board


def setup_pieces(board):
    for i in range(BOARD_SIZE):
        board[1][i] = Pawn(Color.BLACK)
        board[6][i] = Pawn(Color.WHITE)

    piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece in enumerate(piece_order):
        board[0][i] = piece(Color.BLACK)
        board[7][i] = piece(Color.WHITE)
