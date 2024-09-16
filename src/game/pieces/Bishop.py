from typing import List, Optional

from src.game.Aliases import TBoard
from src.game.Constants import BOARD_SIZE
from src.game.pieces.Piece import Piece


class Bishop(Piece):
    def get_valid_moves(self, board: TBoard, position: tuple[int, int]) -> List[tuple[int, int]]:
        valid_moves: List[tuple[int, int]] = []
        x, y = position

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if board[ny][nx] is None:
                    valid_moves.append((nx, ny))
                elif board[ny][nx].color != self.color:
                    valid_moves.append((nx, ny))
                    break
                else:
                    break

                nx += dx
                ny += dy

        return valid_moves
