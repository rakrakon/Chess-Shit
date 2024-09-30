from typing import Tuple, List, Optional, TypeAlias

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.Color import Color
from src.game.TurnManager import TurnManager
from src.game.pieces.Bishop import Bishop
from src.game.pieces.King import King, get_king_moves
from src.game.pieces.Knight import Knight
from src.game.pieces.Pawn import Pawn
from src.game.pieces.Piece import Piece
from src.game.pieces.Queen import Queen
from src.game.pieces.Rook import Rook


class Board:

    def __init__(self):
        self.board: TBoard = create_initial_board()
        self.is_checking = False
        self.has_ended = False
        self.winner: Optional[Color] = None

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

        piece_color = piece.color

        if piece_color != TurnManager().get_current_turn():
            return False

        if piece is None:
            raise ValueError("No piece at the source position")

        y, x = from_pos
        valid_moves = piece.get_valid_moves(self.board, (x, y))

        if (to_col, to_row) not in valid_moves:
            return False

        if self.is_checking:
            if not self.is_valid_defense_move(from_pos, to_pos, piece):
                return False

        piece.move(self, from_pos, to_pos)

        piece.get_valid_moves(self.board, (to_col, to_row))

        if piece.is_checking:
            self.is_checking = True

        TurnManager().next_turn()

        next_turn_color = TurnManager().get_current_turn()

        # Draw
        if not self.get_all_valid_moves(next_turn_color):
            self.has_ended = True

        if self.is_checking and self.is_checkmate(next_turn_color):
            self.has_ended = True
            self.winner = piece.color

        return True

    def get_winner(self):
        return self.winner

    def get_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        row, col = position
        if not is_valid_position(row, col):
            raise ValueError("Invalid position")
        return self.board[row][col]

    def set_piece(self, position: Tuple[int, int], piece: Optional[Piece]):
        row, col = position
        self.board[row][col] = piece

    def remove_piece(self, position: Tuple[int, int]):
        self.set_piece(position, None)

    def get_valid_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        piece = self.get_piece(position)

        if piece is None:
            return []

        return piece.get_valid_moves(self.board, position)

    def update_checks(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.get_piece((y, x))
                if piece is not None:
                    piece.get_valid_moves(self.board, (x, y))
                    if piece.is_checking:
                        return
        self.is_checking = False

    def is_valid_defense_move(self, from_pos, to_pos, piece):
        to_pos_piece = self.get_piece(to_pos)
        piece.move(self, from_pos, to_pos)
        self.update_checks()
        is_valid = not self.is_checking
        piece.move(self, to_pos, from_pos)
        self.set_piece(to_pos, to_pos_piece)
        return is_valid

    def is_checkmate(self, color) -> bool:
        all_moves = self.get_all_valid_moves(color)
        for piece in all_moves:
            from_to = (piece[0][1], piece[0][0])
            for valid_move in piece[1]:
                valid_move = (valid_move[1], valid_move[0])
                if self.is_valid_defense_move(from_to, valid_move, self.get_piece(from_to)):
                    return False
        return True

    # Color of the next turn - Example: If white checkmates black, Color black will be passed
    def get_all_valid_moves(self, color: Color) -> List[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        all_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                position = (row, col)
                piece = self.get_piece(position)

                if not isinstance(piece, Piece) or piece.color != color:
                    continue

                piece_moves = piece.get_valid_moves(self.board, (col, row))
                if piece_moves:
                    all_moves.append(((col, row), piece_moves)) # Position tuple is in (x,y) piece moves is (x,y)
        return all_moves

    def promote_pawn(self, pos, piece_name):
        pawn = self.get_piece(pos)
        new_piece = None
        print(f"Piece Name is: {piece_name}")
        if piece_name == '♛':
            from src.game.pieces.Queen import Queen
            new_piece = Queen(pawn.color)
        elif piece_name == '♜':
            from src.game.pieces.Rook import Rook
            new_piece = Rook(pawn.color)
        elif piece_name == '♝':
            from src.game.pieces.Bishop import Bishop
            new_piece = Bishop(pawn.color)
        elif piece_name == '♞':
            from src.game.pieces.Knight import Knight
            new_piece = Knight(pawn.color)

        self.remove_piece(pos)
        self.set_piece(pos, new_piece)


def is_valid_position(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def create_initial_board() -> TBoard:
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    setup_pieces(board)

    return board


def setup_pieces(board):
    for i in range(BOARD_SIZE):
        board[Color.BLACK.starting_row][i] = Pawn(Color.BLACK)
        board[Color.WHITE.starting_row][i] = Pawn(Color.WHITE)

    piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for i, piece in enumerate(piece_order):
        board[Color.WHITE.opposite_row][i] = piece(Color.BLACK)
        board[Color.BLACK.opposite_row][i] = piece(Color.WHITE)
