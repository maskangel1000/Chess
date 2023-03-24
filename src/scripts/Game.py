import pygame

import Move

WIDTH = 512
HEIGHT = 512

LIGHT = (227, 209, 200)
DARK = (112, 92, 69)

def draw_squares(screen, board):
    is_white = True
    for x in range(0, len(board.board)):
        for y in range(0, len(board.board[x])):
            square = pygame.rect.Rect(x*64, y*64, 64, 64)
            if is_white:
                pygame.draw.rect(screen, LIGHT, square)
            else:
                pygame.draw.rect(screen, DARK, square)
            is_white = not is_white
        is_white = not is_white

def draw_pieces(screen, board):
    for row in range(0, len(board.board)):
        for col in range(0, len(board.board[row])):
            if board.board[row][col]:
                piece_name = board.board[row][col].color + board.board[row][col].type
                piece_image = pygame.image.load(f"../assets/{piece_name}.png")
                screen.blit(piece_image, (col*64 + 3, row*64 + 3))
    
def get_mouse_square(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // 64) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return board.board[y][x], x, y
    except IndexError:
        return None, None, None
    
def draw_selector(screen, piece, x, y):
    if piece:
        rect = (x * 64, y * 64, 64, 64)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def main(board):

    # Init

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Chess")

    # Objects

    icon = pygame.image.load("../assets/icon.svg")

    # Variables

    selected_piece = None
    dragging = False

    # Main

    clock = pygame.time.Clock()

    running = True

    while running:

        # Events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                if piece:
                    selected_piece = piece, x, y
            
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    piece, old_x, old_y = selected_piece
                    Move.move(board, old_x, old_y, x, y)
                dragging = False

        # Draws

        pygame.display.flip()
        pygame.display.set_icon(icon)

        # Updates

        if not dragging: selected_piece = None

        piece, x, y = get_mouse_square(board)

        draw_squares(screen, board)
        draw_pieces(screen, board)
        draw_selector(screen, piece, x, y)

        # Clock

        clock.tick()

# End

pygame.quit()