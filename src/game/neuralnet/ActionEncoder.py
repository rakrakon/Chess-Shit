TOTAL_SQUARES = 64
PROMOTION_PIECES = ['Q', 'R', 'B', 'N']  # Queen, Rook, Bishop, Knight
PROMOTION_OFFSET = TOTAL_SQUARES * TOTAL_SQUARES  # moves without promotion use 0–4095

def encode_move(from_pos: tuple[int, int], to_pos: tuple[int, int], promotion: str | None = None) -> int:
    """
    Encode a move as an integer index.
    from_pos, to_pos: (row, col) tuples
    promotion: 'Q', 'R', 'B', 'N' or None
    """
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    from_index = from_row * 8 + from_col
    to_index = to_row * 8 + to_col

    if promotion is None:
        return from_index * TOTAL_SQUARES + to_index
    else:
        # promotion moves start after all normal moves
        promotion_index = PROMOTION_PIECES.index(promotion.upper())
        return PROMOTION_OFFSET + (from_index * len(PROMOTION_PIECES)) + promotion_index


def decode_action(index: int) -> tuple[tuple[int, int], tuple[int, int], str | None]:
    """
    Decode an integer index back to a move.
    Returns: (from_pos, to_pos, promotion)
    """
    if index < PROMOTION_OFFSET:
        from_index = index // TOTAL_SQUARES
        to_index = index % TOTAL_SQUARES
        from_pos = (from_index // 8, from_index % 8)
        to_pos = (to_index // 8, to_index % 8)
        return from_pos, to_pos, None
    else:
        index -= PROMOTION_OFFSET
        from_index = index // len(PROMOTION_PIECES)
        promotion_index = index % len(PROMOTION_PIECES)
        promotion = PROMOTION_PIECES[promotion_index]
        from_pos = (from_index // 8, from_index % 8)
        to_pos = None
        return from_pos, to_pos, promotion


def total_actions() -> int:
    """
    Total number of actions in the fixed action space
    """
    return PROMOTION_OFFSET + TOTAL_SQUARES * len(PROMOTION_PIECES)