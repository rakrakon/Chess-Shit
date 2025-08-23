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

    def draw_winning_screen(self):
        winner = self.board.winner
        if not winner:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((30, 30, 30))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        button_font = pygame.font.SysFont("Arial", 32)

        # Draw winner text
        text = f"{winner.name} Wins!"
        text_surface = title_font.render(text, True, (240, 240, 240))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(text_surface, text_rect)

        # Button properties
        button_width = 220
        button_height = 60
        spacing = 20
        button_color = (60, 60, 60)
        hover_color = (90, 90, 90)
        text_color = (255, 255, 255)

        restart_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        quit_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_height + spacing, button_width,
                                button_height)

        mouse_pos = pygame.mouse.get_pos()
        restart_current_color = hover_color if restart_rect.collidepoint(mouse_pos) else button_color
        quit_current_color = hover_color if quit_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, restart_current_color, restart_rect, border_radius=15)
        pygame.draw.rect(screen, quit_current_color, quit_rect, border_radius=15)

        restart_text_surface = button_font.render("Restart", True, text_color)
        quit_text_surface = button_font.render("Quit", True, text_color)

        restart_text_rect = restart_text_surface.get_rect(center=restart_rect.center)
        quit_text_rect = quit_text_surface.get_rect(center=quit_rect.center)

        screen.blit(restart_text_surface, restart_text_rect)
        screen.blit(quit_text_surface, quit_text_rect)

        return restart_rect, quit_rect

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

    def reset_game(self):
        self.board = Board()
        self.selected_piece = None
        self.promotion_menu_active = False

    def run(self):
        clock = pygame.time.Clock()
        restart_btn = None
        quit_btn = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.board.has_ended:
                        if restart_btn and restart_btn.collidepoint(event.pos):
                            self.reset_game()
                        elif quit_btn and quit_btn.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    else:
                        self.handle_click(event.pos)

            screen.fill(PIECE_OUTLINE_BLACK)
            self.draw_board()

            if self.promotion_menu_active:
                self.draw_promotion_menu()

            if self.board.has_ended:
                restart_btn, quit_btn = self.draw_winning_screen()

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    game = ChessGame()
    game.run()
