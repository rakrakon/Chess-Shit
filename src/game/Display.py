import sys
import pygame

from src.game.Board import Board
from src.game.Color import Color
from src.game.Constants import *
from src.game.pieces.Pawn import Pawn

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)


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
        self.promotion_menu_active = False
        self.promotion_pawn_pose = (0,0)

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

                piece = self.board.get_piece((row, col))
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

    def draw_promotion_menu(self):
        pieces = ["♛", "♜", "♝", "♞"]

        spacing = 55
        total_height = len(pieces) * spacing
        total_width = 40

        row, col = self.promotion_pawn_pose

        start_x = col * SQUARE_SIZE
        start_y = row * SQUARE_SIZE

        if start_y + total_height > HEIGHT:
            start_y = HEIGHT - total_height

        pygame.draw.rect(screen, WHITE, (start_x, start_y, total_width, total_height))

        piece_rects = []
        for i, piece in enumerate(pieces):
            text_surface = self.font.render(piece, True, BLACK)
            text_rect = text_surface.get_rect(center=(start_x + total_width // 2, start_y + i * spacing + spacing // 2))
            screen.blit(text_surface, text_rect)
            piece_rects.append((piece, text_rect))

        return piece_rects

    def handle_click(self, pos):
        if self.promotion_menu_active:
            piece_rects = self.draw_promotion_menu()
            for piece_name, rect in piece_rects:
                if rect.collidepoint(pos):
                    self.board.promote_pawn(self.promotion_pawn_pose, piece_name)
                    self.promotion_menu_active = False
                    self.promotion_pawn_pose = None
                    return

        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_piece:
            self.board.move_piece(self.selected_piece, (row, col))
            piece = self.board.get_piece((row, col))
            if type(piece) == Pawn and piece.color.opposite_row == row:
                self.promotion_menu_active = True
                self.promotion_pawn_pose = (row, col)
            self.selected_piece = None
        else:
            if self.board.get_piece((row, col)):
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

            if self.promotion_menu_active:
                self.draw_promotion_menu()

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    game = ChessGame()
    game.run()
