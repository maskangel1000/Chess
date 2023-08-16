import pygame
import tkinter as tk

import Move

LIGHT = (227, 209, 200)
DARK = (112, 92, 69)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = round(screen_width/3.072)
height = round(screen_height/1.728)

typing_width = False
typing_height = False

temp_width = str(width)
temp_height = str(height)

def draw_squares(screen, board):
    global width, height
    
    is_white = True
    for x in range(0, len(board.board)):
        for y in range(0, len(board.board[x])):
            square = pygame.rect.Rect(x*width/8, y*height/8, width/8, height/8)
            if is_white:
                pygame.draw.rect(screen, LIGHT, square)
            else:
                pygame.draw.rect(screen, DARK, square)
            is_white = not is_white
        is_white = not is_white

def draw_pieces(screen, board, dragging, selected_piece):
    global width, height
    
    drag_queue = None
    for row in range(0, len(board.board)):
        for col in range(0, len(board.board[row])):
            if board.board[row][col]:
                piece_name = board.board[row][col].color + board.board[row][col].type
                piece_image = pygame.image.load(f"../assets/{piece_name}.png")
                piece_image = pygame.transform.scale(piece_image, (width//8, height//8))
                if dragging and selected_piece and selected_piece[1] == col and selected_piece[2] == row:
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    mouse_x, mouse_y = mouse_pos
                    drag_queue = piece_image
                else:
                    screen.blit(piece_image, (col*width/8, row*height/8))
    if drag_queue:
        screen.blit(drag_queue, (mouse_x - (width//8) / 2, mouse_y - (height//8) / 2))
    
def get_mouse_square(board):
    global width, height
    
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x = int(mouse_pos[0] // (width/8))
    y = int(mouse_pos[1] // (height/8))
    try:
        if x >= 0 and y >= 0:
            return board.board[y][x], x, y
    except IndexError:
        return None, None, None
    
def draw_selector(board, screen, piece, x, y, dragging, selected_piece):
    global width, height
    
    if x == None or y == None:
        return
    rect = (x*width/8, y*height/8, width/8, height/8)
    if dragging and selected_piece and selected_piece[0]:
        if Move.is_legal(board, selected_piece[1], selected_piece[2], x, y):
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, width//130)
        else:
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, width//130)
    elif piece and piece.color == board.turn:
        pygame.draw.rect(screen, (0, 255, 0, 50), rect, width//130)

def end_game(screen, loser, board):
    global width, height
    
    draw_squares(screen, board)
    draw_pieces(screen, board, None, None)

    winner = "White" if loser == 'b' else "Black"
    same_color = (195, 195, 195) if winner == "White" else (60, 60, 60)
    opposite_color = (60, 60, 60) if winner == "White" else (195, 195, 195)

    background = pygame.Surface((width, height))
    background.set_alpha(200)
    background.fill(same_color)
    screen.blit(background, (0, 0))

    button = pygame.Surface((200, 50))
    button.set_alpha(150)
    button.fill(opposite_color)
    screen.blit(button, (width/2-100, height/2))

    menu_button = pygame.Surface((200, 50))
    menu_button.set_alpha(150)
    menu_button.fill(opposite_color)
    screen.blit(menu_button, (width/2-100, height/2+height/7))

    font = pygame.font.SysFont("Arial", 30)

    win_text = font.render(f"{winner} wins!", True, opposite_color)
    screen.blit(win_text, (width/2-75, height/2-50))

    play_text = font.render("PLAY AGAIN", True, same_color)
    screen.blit(play_text, (width/2-85, height/2+10))

    menu_text = font.render("MENU", True, same_color)
    screen.blit(menu_text, (width/2-85, height/2+10+height/7))
    
def draw_menu(screen):
    global width, height
    
    background = pygame.Surface((width, height))
    background.set_alpha(200)
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    play_button = pygame.Surface((200, 50))
    play_button.set_alpha(150)
    play_button.fill((255, 255, 255))
    screen.blit(play_button, (width/2-100, height/2-height/10))
    
    settings_button = pygame.Surface((200, 50))
    settings_button.set_alpha(150)
    settings_button.fill((255, 255, 255))
    screen.blit(settings_button, (width/2-100, height/2+height/10))
    
    font = pygame.font.SysFont("Arial", 40)

    play_text = font.render("PLAY", True, (0, 0, 0))
    screen.blit(play_text, (width/2-85, height/2-height/10))
    
    settings_text = font.render("SETTINGS", True, (0, 0, 0))
    screen.blit(settings_text, (width/2-85, height/2+height/10))
    
def draw_settings(screen):
    global width, height, temp_width, temp_height
    
    background = pygame.Surface((width, height))
    background.set_alpha(200)
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    back_button = pygame.Surface((100, 50))
    back_button.set_alpha(150)
    back_button.fill((255, 255, 255))
    screen.blit(back_button, (width/50, height/50))
    
    apply_button = pygame.Surface((110, 50))
    apply_button.set_alpha(150)
    apply_button.fill((255, 255, 255))
    screen.blit(apply_button, (width - width/50 - 110, height/50))
    
    width_button = pygame.Surface((200, 50))
    width_button.set_alpha(150)
    width_button.fill((255, 255, 255))
    screen.blit(width_button, (width/2-100, height/2+height/10))
    
    height_button = pygame.Surface((200, 50))
    height_button.set_alpha(150)
    height_button.fill((255, 255, 255))
    screen.blit(height_button, (width/2-100, height/2-height/10))
    
    font = pygame.font.SysFont("Arial", 40)
    
    back_text = font.render("BACK", True, (0, 0, 0))
    screen.blit(back_text, (width/35, height/50))
    
    apply_text = font.render("APPLY", True, (0, 0, 0))
    screen.blit(apply_text, (width - width/35 - 100, height/50))

    width_text = font.render("WIDTH", True, (255, 255, 255))
    screen.blit(width_text, (width/2-85, height/2-height/5))
    
    height_text = font.render("HEIGHT", True, (255, 255, 255))
    screen.blit(height_text, (width/2-85, height/2+height/5))

    width_number = font.render(temp_width, True, (0, 0, 0))
    screen.blit(width_number, (width/2-85, height/2-height/10))
    
    height_number = font.render(temp_height, True, (0, 0, 0))
    screen.blit(height_number, (width/2-85, height/2+height/10))

def main(board):
    global width, height, temp_width, temp_height

    # Init

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Chess")

    # Objects

    icon = pygame.image.load("../assets/icon.svg")

    # Variables

    selected_piece = None
    dragging = False

    # Main

    clock = pygame.time.Clock()

    running = True
    menu = True
    settings = False
    checkmate = False
    checkmate_button = False

    while running:
        # Events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if menu == False and settings == False:
                    menu = True
                else:
                    running = False
                    continue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                mouse = pygame.mouse.get_pos()
                if checkmate:
                    if width/2-100 <= mouse[0] <= width/2+100 and height/2 <= mouse[1] <= height/2+50:
                        board.reset_board()
                        checkmate = False
                        selected_piece = None
                    if width/2-100 <= mouse[0] <= width/2+100 and height/2+height/7 <= mouse[1] <= height/2+50+height/7:
                        board.reset_board()
                        checkmate = False
                        selected_piece = None
                        menu = True
                elif menu:
                    if width/2-100 <= mouse[0] <= width/2+100 and height/2-height/10 <= mouse[1] <= height/2-height/10+50:
                        menu = False
                    if width/2-100 <= mouse[0] <= width/2+100 and height/2+height/10 <= mouse[1] <= height/2+height/10+50:
                        menu = False
                        settings = True
                        temp_width = str(width)
                        temp_height = str(height)
                elif settings:
                    if width/2-100 <= mouse[0] <= width/2+100 and height/2-height/10 <= mouse[1] <= height/2-height/10+50:
                        typing_width = True
                        typing_height = False
                    elif width/2-100 <= mouse[0] <= width/2+100 and height/2+height/10 <= mouse[1] <= height/2+height/10+50:
                        typing_height = True
                        typing_width = False
                    else:
                        typing_width = False
                        typing_height = False
                        if width/50 <= mouse[0] <= width/50+100 and height/50 <= mouse[1] <= height/50+50:
                            settings = False
                            menu = True
                        elif width - width/50 - 110 <= mouse[0] <= width - width/50 and height/50 <= mouse[1] <= height/50+50:
                            try:
                                width = int(temp_width)
                                height = int(temp_height)
                                main(board)
                            except ValueError:
                                temp_width = str(width)
                                temp_height = str(height)
                elif piece:
                    selected_piece = piece, x, y
                    
            if event.type == pygame.KEYDOWN:
                if event.key != 8 and (event.key < 48 or event.key > 57):
                    continue
                
                if typing_width:
                    if event.key == 8:
                        temp_width = temp_width[:-1]
                    else:
                        temp_width += chr(event.key)
                if typing_height:
                    if event.key == 8:
                        temp_height = temp_height[:-1]
                    else:
                        temp_height += chr(event.key)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_piece and not checkmate:
                    if x == None or y == None:
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

        if running == False:
            pygame.quit()
        
        # Draws

        pygame.display.flip()
        pygame.display.set_icon(icon)

        # Updates

        draw_squares(screen, board)
        
        if not checkmate and not menu and not settings:
            
            if not dragging: selected_piece = None

            try:
                piece, x, y = get_mouse_square(board)
            except TypeError:
                continue

            draw_selector(board, screen, piece, x, y, dragging, selected_piece)            
        
        draw_pieces(screen, board, dragging, selected_piece)
        
        if menu:
            draw_menu(screen)
            
        if settings:
            draw_settings(screen)
            
        if checkmate:
            end_game(screen, board.turn, board)

        # Clock

        clock.tick()

# End

pygame.quit()