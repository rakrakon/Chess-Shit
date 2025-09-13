import time

import pygame
from src.game.Board import Board
from src.game.Color import Color
from src.game.Constants import *
from src.game.Display import ChessGame
from src.game.neuralnet.ActionEncoder import decode_action, encode_move

# Piece symbols
piece_symbols = {
    'Pawn': '♟',
    'Rook': '♜',
    'Knight': '♞',
    'Bishop': '♝',
    'Queen': '♛',
    'King': '♚'
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

def draw_piece(screen, font, piece, x, y):
    piece_type = type(piece).__name__
    symbol = piece_symbols[piece_type][0]

    if piece.color == Color.WHITE:
        outline = font.render(symbol, True, PIECE_OUTLINE_BLACK)
        fill = font.render(symbol, True, PIECE_WHITE)
    else:
        outline = font.render(symbol, True, PIECE_OUTLINE_BLACK)
        fill = font.render(symbol, True, PIECE_BLACK)

    outline_rect = outline.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
    fill_rect = fill.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))

    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        screen.blit(outline, (outline_rect.x + dx, outline_rect.y + dy))

    screen.blit(fill, fill_rect)


def draw_board(screen, font, board, selected_piece=None):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = BOARD_WHITE if (row + col) % 2 == 0 else BOARD_GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.get_piece((row, col))
            if piece:
                draw_piece(screen, font, piece, col * SQUARE_SIZE, row * SQUARE_SIZE)

    if selected_piece:
        row, col = selected_piece
        pygame.draw.rect(
            screen, HIGHLIGHT,
            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            4
        )


def debug_draw_board(board):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Debug Chess Board")
    font = pygame.font.SysFont('segoeuisymbol', 48)

    # Draw board once
    draw_board(screen, font, board)
    pygame.display.flip()

    # Keep window open until user closes
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.wait(50)

    pygame.quit()

def visualize_game():
    game = ChessGame()
    game.board.move_piece()

if __name__ == '__main__':
    # print(encode_move((6,5), (7,4)))
    # print(decode_action(267))
    # valid_moves = [((0, 4), [(0, 3)]), ((4, 4), [(4, 3)]), ((0, 5), [(1, 3), (1, 7), (2, 4)]), ((3, 5), [(3, 4)]), ((5, 5), [(5, 4)]), ((1, 6), [(1, 5)]), ((2, 6), [(2, 5), (2, 4)]), ((5, 6), [(4, 5), (4, 6), (4, 7), (5, 7)]), ((6, 6), [(6, 5), (6, 4)]), ((7, 6), [(7, 5), (7, 4)]), ((0, 7), [(1, 7), (0, 6)]), ((2, 7), [(3, 6), (4, 5), (5, 4), (6, 3), (7, 2)]), ((3, 7), [(4, 7), (3, 6), (4, 6)]), ((5, 7), [(4, 6)]), ((6, 7), [(4, 6), (7, 5)])]
    # for from_pos, moves in valid_moves:
    #     for move in moves:
    #         move_id = encode_move(from_pos, move)
    #         print(move_id)
    pass