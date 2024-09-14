from typing import List, Optional

from src.game.pieces.Piece import Piece


class Knight(Piece):
    def get_valid_moves(self, board: List[List[Optional[Piece]]], position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []
        x, y = position
        knight_moves = [
            (x - 2, y - 1), (x - 2, y + 1),
            (x - 1, y - 2), (x - 1, y + 2),
            (x + 1, y - 2), (x + 1, y + 2),
            (x + 2, y - 1), (x + 2, y + 1)
        ]

        for move in knight_moves:
            new_x, new_y = move
            board_length = len(board)
            if 0 <= new_x < board_length and 0 <= new_y < board_length:
                if board[new_x][new_y] is None or board[new_x][new_y].color != self.color:
                    valid_moves.append(move)

        return valid_moves
