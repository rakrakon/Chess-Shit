import sys

import pygame

from src.game.Board import Board
from src.game.Color import Color
from src.game.Constants import *


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.board.print_board()
        self.selected_piece = None
        self.font = pygame.font.SysFont('segoeuisymbol', 48)
        self.piece_symbols = {
            'Pawn': '♟',
            'Rook': '♜',
            'Knight': '♞',
            'Bishop': '♝',
            'Queen': '♛',
            'King': '♚'
        }

    def draw_piece(self, piece, x, y):
        piece_type = type(piece).__name__
        symbol = self.piece_symbols[piece_type][0]

        if piece.color == Color.WHITE:
            outline = self.font.render(symbol, True, PIECE_OUTLINE_BLACK)
            fill = self.font.render(symbol, True, PIECE_WHITE)
        else:
            outline = self.font.render(symbol, True, PIECE_OUTLINE_BLACK)
            fill = self.font.render(symbol, True, PIECE_BLACK)

        outline_rect = outline.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
        fill_rect = fill.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            screen.blit(outline, (outline_rect.x + dx, outline_rect.y + dy))

        screen.blit(fill, fill_rect)

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = BOARD_WHITE if (row + col) % 2 == 0 else BOARD_GREEN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board.get_piece(row, col)
                if piece:
                    self.draw_piece(piece, col * SQUARE_SIZE, row * SQUARE_SIZE)

        if self.selected_piece:
            row, col = self.selected_piece
            pygame.draw.rect(
                screen, HIGHLIGHT,
                (
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE
                ),
                4
            )

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_piece:
            self.board.move_piece(self.selected_piece, (row, col))
            self.selected_piece = None
        else:
            if self.board.get_piece(row, col):
                self.selected_piece = (row, col)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            screen.fill(PIECE_OUTLINE_BLACK)
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    game = ChessGame()
    game.run()
