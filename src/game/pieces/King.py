from typing import List, Optional

from src.game.pieces.Piece import Piece


class King(Piece):
    def get_valid_moves(self, board, position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []
        x, y = position
        king_moves = [
            (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
        ]

        board_length = len(board)

        for move in king_moves:
            new_x, new_y = move
            if 0 <= new_x < board_length and 0 <= new_y < board_length:
                if board[new_x][new_y] is None or board[new_x][new_y].color != self.color:
                    valid_moves.append(move)

        # TODO: Implement castling logic

        return valid_moves
