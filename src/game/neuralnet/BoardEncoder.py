import numpy as np
from src.game.pieces.Pawn import Pawn
from src.game.pieces.Knight import Knight
from src.game.pieces.Bishop import Bishop
from src.game.pieces.Rook import Rook
from src.game.pieces.Queen import Queen
from src.game.pieces.King import King
from src.game.Color import Color

# Piece planes
PIECE_TO_PLANE = {
    Pawn: 0,
    Knight: 1,
    Bishop: 2,
    Rook: 3,
    Queen: 4,
    King: 5
}

def encode_board(board):
    # Fill piece planes based on board
    planes = np.zeros((8, 8, 13), dtype=np.float32)
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                base_plane = PIECE_TO_PLANE[type(piece)]
                if piece.color == Color.WHITE:
                    planes[row, col, base_plane] = 1
                else:
                    planes[row, col, base_plane + 6] = 1

    # Fill Side to move plane
    planes[:, :, 12] = 1 if board.get_current_turn() == Color.WHITE else 0
    return planes