from src.game.Color import Color
from src.game.Constants import Constants
from src.game.pieces.Bishop import Bishop
from src.game.pieces.King import King
from src.game.pieces.Knight import Knight
from src.game.pieces.Pawn import Pawn
from src.game.pieces.Queen import Queen
from src.game.pieces.Rook import Rook


class Board:
    def __init__(self):
        self.board = create_initial_board()

    def print_board(self):
        for row in self.board:
            print(" | ".join([str(piece) if piece else " " for piece in row]))
            print("-" * 33)


def create_initial_board():
    board = [[None for _ in range(Constants.BOARD_SIZE)] for _ in range(Constants.BOARD_SIZE)]

    setup_pieces(board)

    return board


def setup_pieces(board):
    for i in range(Constants.BOARD_SIZE):
        board[1][i] = Pawn(Color.WHITE)
        board[6][i] = Pawn(Color.BLACK)

    piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece in enumerate(piece_order):
        board[0][i] = piece(Color.WHITE)
        board[7][i] = piece(Color.BLACK)
