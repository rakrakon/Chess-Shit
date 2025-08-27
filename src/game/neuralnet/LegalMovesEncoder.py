from ActionEncoder import encode_move, PROMOTION_PIECES
from src.game.Board import Board
from src.game.pieces.Pawn import Pawn


def board_legal_action_indices(board: Board) -> list[int]:
    action_indices = []
    all_moves = board.get_all_valid_moves(board.get_current_turn())  # {(from_col, from_row): [(to_col, to_row), ...]}

    for (from_col, from_row), moves in all_moves:
        piece = board.get_piece((from_row, from_col))  # Convert to (row, col) for board.get_piece
        if piece is None:
            continue

        for to_col, to_row in moves:
            from_pos = (from_row, from_col)  # (row, col)
            to_pos = (to_row, to_col)        # (row, col)

            # Handle pawn promotion
            if isinstance(piece, Pawn) and piece.color.opposite_row == to_row:
                for promo in PROMOTION_PIECES:
                    idx = encode_move(from_pos, to_pos, promotion=promo)
                    action_indices.append(idx)
                continue

            # Normal move
            idx = encode_move(from_pos, to_pos)
            action_indices.append(idx)

    return action_indices
