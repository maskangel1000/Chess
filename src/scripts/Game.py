import pygame

import Move

WIDTH = 500
HEIGHT = 500

LIGHT = (227, 209, 200)
DARK = (112, 92, 69)

def draw_squares(screen, board):
    is_white = True
    for x in range(0, len(board.board)):
        for y in range(0, len(board.board[x])):
            square = pygame.rect.Rect(x*WIDTH/8, y*HEIGHT/8, WIDTH/8, HEIGHT/8)
            if is_white:
                pygame.draw.rect(screen, LIGHT, square)
            else:
                pygame.draw.rect(screen, DARK, square)
            is_white = not is_white
        is_white = not is_white

def draw_pieces(screen, board, dragging, selected_piece):
    drag_queue = None
    for row in range(0, len(board.board)):
        for col in range(0, len(board.board[row])):
            if board.board[row][col]:
                piece_name = board.board[row][col].color + board.board[row][col].type
                piece_image = pygame.image.load(f"../assets/{piece_name}.png")
                piece_image = pygame.transform.scale(piece_image, (WIDTH//8, HEIGHT//8))
                if dragging and selected_piece and selected_piece[1] == col and selected_piece[2] == row:
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    mouse_x, mouse_y = mouse_pos
                    drag_queue = piece_image
                else:
                    screen.blit(piece_image, (col*WIDTH/8, row*HEIGHT/8))
    if drag_queue:
        screen.blit(drag_queue, (mouse_x - (WIDTH//8) / 2, mouse_y - (HEIGHT//8) / 2))
    
def get_mouse_square(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x = int(mouse_pos[0] // (WIDTH/8))
    y = int(mouse_pos[1] // (HEIGHT/8))
    try:
        if x >= 0 and y >= 0:
            return board.board[y][x], x, y
    except IndexError:
        return None, None, None
    
def draw_selector(board, screen, piece, x, y, dragging, selected_piece):
    if not x or not y:
        return
    rect = (x*WIDTH/8, y*HEIGHT/8, WIDTH/8, HEIGHT/8)
    if dragging and selected_piece and selected_piece[0]:
        if Move.is_legal(board, selected_piece[1], selected_piece[2], x, y):
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, WIDTH//170)
        else:
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, WIDTH//170)
    elif piece and piece.color == board.turn:
        pygame.draw.rect(screen, (0, 255, 0, 50), rect, WIDTH//170)
    else:
        print(1)

def end_game(screen, loser, board):
    draw_squares(screen, board)
    draw_pieces(screen, board, None, None)

    winner = "White" if loser == 'b' else "Black"
    same_color = (195, 195, 195) if winner == "White" else (60, 60, 60)
    opposite_color = (60, 60, 60) if winner == "White" else (195, 195, 195)

    background = pygame.Surface((WIDTH, HEIGHT))
    background.set_alpha(200)
    background.fill(same_color)
    screen.blit(background, (0, 0))

    button = pygame.Surface((200, 50))
    button.set_alpha(150)
    button.fill(opposite_color)
    screen.blit(button, (WIDTH/2-100, HEIGHT/2))

    font = pygame.font.SysFont("Arial", 30)

    win_text = font.render(f"{winner} wins!", True, opposite_color)
    screen.blit(win_text, (WIDTH/2-75, HEIGHT/2-50))

    play_text = font.render("PLAY AGAIN", True, same_color)
    screen.blit(play_text, (WIDTH/2-85, HEIGHT/2+10))

def main(board):

    # Init

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

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
    checkmate = False
    checkmate_button = False

    while running:

        # Events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                if checkmate:
                    mouse = pygame.mouse.get_pos()
                    if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+50:
                        checkmate_button = True
                elif piece:
                    selected_piece = piece, x, y
            
            if event.type == pygame.MOUSEBUTTONUP:
                if checkmate_button:
                    mouse = pygame.mouse.get_pos()
                    if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+50:
                        board.reset_board()
                        checkmate = False
                        checkmate_button = False
                        selected_piece = None

                elif selected_piece and not checkmate:
                    if not x or not y:
                        continue
                    
                    piece, old_x, old_y = selected_piece
                    capture, castle, check = False, False, False

                    if board.board[y][x] or (board.enpassant_x == x and board.enpassant_y == y):
                        capture = True
                    if board.board[old_y][old_x].type == 'k' and abs(x-old_x) > 1:
                        castle = True

                    if Move.move(board, old_x, old_y, x, y):

                        if not Move.check_check(board, 0, 0, 0, 0):
                            check = True
                            if Move.is_checkmate(board):
                                checkmate = True
                                end_game(screen, board.turn, board)

                        if check:
                            sound = pygame.mixer.Sound("../assets/check.mp3")
                            pygame.mixer.Sound.play(sound)
                        elif capture:
                            sound = pygame.mixer.Sound("../assets/capture.mp3")
                            pygame.mixer.Sound.play(sound)
                        elif castle:
                            sound = pygame.mixer.Sound("../assets/castle.mp3")
                            pygame.mixer.Sound.play(sound)
                        else:
                            sound = pygame.mixer.Sound("../assets/move.mp3")
                            pygame.mixer.Sound.play(sound)

                    dragging = False

        # Draws

        pygame.display.flip()
        pygame.display.set_icon(icon)

        # Updates
        

        if not checkmate:

            if not dragging: selected_piece = None

            try:
                piece, x, y = get_mouse_square(board)
            except TypeError:
                continue

            draw_squares(screen, board)
            draw_selector(board, screen, piece, x, y, dragging, selected_piece)
            draw_pieces(screen, board, dragging, selected_piece)

        # Clock

        clock.tick()

# End

pygame.quit()
