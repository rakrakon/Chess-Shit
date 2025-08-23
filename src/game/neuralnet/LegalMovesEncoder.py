from ActionEncoder import encode_move, PROMOTION_PIECES
from src.game.Board import Board
from src.game.pieces.Pawn import Pawn
from src.game.Constants import BOARD_SIZE


def board_legal_action_indices(board: Board) -> list[int]:
    action_indices = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece((row, col))
            if piece is None or piece.color != board.get_current_turn():
                continue

            valid_moves = board.get_valid_moves((row, col))

            for to_col, to_row in valid_moves:
                to_pos = (to_row, to_col)  # encode_move expects (row, col)

                # Handle pawn promotion
                if isinstance(piece, Pawn):
                    if piece.color.opposite_row == to_row:
                        for promo in PROMOTION_PIECES:
                            idx = encode_move((row, col), to_pos, promotion=promo)
                            action_indices.append(idx)
                        continue

                # Normal move
                idx = encode_move((row, col), to_pos)
                action_indices.append(idx)

    return action_indices
