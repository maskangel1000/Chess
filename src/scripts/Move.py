import copy

from Piece import Piece

def check_turn(board, old_x, old_y):
    return True if board.board[old_y][old_x].color == board.turn else False

def check_same(board, old_x, old_y, new_x, new_y):

    offset_x = abs(new_x - old_x)
    offset_y = abs(new_y - old_y)

    return True if offset_x != 0 or offset_y != 0 else False

def check_capture(board, old_x, old_y, new_x, new_y):

    if not board.board[new_y][new_x]:
        return True
    
    old_color = board.board[old_y][old_x].color
    new_color = board.board[new_y][new_x].color

    if old_color != new_color:
        return True
    
    return False

def check_check(board, old_x, old_y, new_x, new_y):
    new_board = copy.deepcopy(board)
    new_board.board[new_y][new_x] = new_board.board[old_y][old_x]
    new_board.board[old_y][old_x] = None

    for row in range(0, len(new_board.board)):
        for col in range(0, len(new_board.board[row])):
            piece = new_board.board[row][col]
            if piece and piece.color == board.turn and piece.type == 'k':
                king_x = col
                king_y = row

    for y in range(0, len(new_board.board)):
        for x in range(0, len(new_board.board[y])):
            piece = new_board.board[y][x]
            if piece and piece.color != board.turn:
                if is_legal(new_board, x, y, king_x, king_y, check=True):
                    return False
    
    return True

def check_bishop(board, old_x, old_y, new_x, new_y):

    offset_x = abs(new_x - old_x)
    offset_y = abs(new_y - old_y)

    if offset_x == offset_y:
        y = old_y
        x = old_x
        if old_x < new_x:
            if old_y < new_y:
                while y < new_y-1 and x < new_x-1:
                    y += 1
                    x += 1
                    if board.board[y][x]:
                        return False
                return True
            if old_y > new_y:
                while y > new_y+1 and x < new_x-1:
                    y -= 1
                    x += 1
                    if board.board[y][x]:
                        return False
                return True
        if old_x > new_x:
            if old_y < new_y:
                while y < new_y-1 and x > new_x+1:
                    y += 1
                    x -= 1
                    if board.board[y][x]:
                        return False
                return True
            if old_y > new_y:
                while y > new_y+1 and x > new_x+1:
                    y -= 1
                    x -= 1
                    if board.board[y][x]:
                        return False
                return True
    
    return False

def check_rook(board, old_x, old_y, new_x, new_y):

    offset_x = abs(new_x - old_x)
    offset_y = abs(new_y - old_y)

    if offset_x == 0 and offset_y != 0:
        y_range = range(old_y+1, new_y) if old_y < new_y else range(old_y-1, new_y, -1)
        for y in y_range:
            if board.board[y][old_x]:
                return False
        return True
    
    if offset_x != 0 and offset_y == 0:
        x_range = range(old_x+1, new_x) if old_x < new_x else range(old_x-1, new_x, -1)
        for x in x_range:
            if board.board[old_y][x]:
                return False
        return True
    
    return False

def check_king(board, old_x, old_y, new_x, new_y):

    offset_x = abs(new_x - old_x)
    offset_y = abs(new_y - old_y)
    
    if offset_x <= 1 and offset_y <= 1:
        return True
    
    return False

def check_knight(old_x, old_y, new_x, new_y):

    offset_x = abs(new_x - old_x)
    offset_y = abs(new_y - old_y)

    if offset_x == 2 and offset_y == 1:
        return True
    
    if offset_x == 1 and offset_y == 2:
        return True
    
    return False

def check_pawn(board, old_x, old_y, new_x, new_y):

    color = board.board[old_y][old_x].color

    if old_x == new_x:
        if not board.board[new_y][new_x]:
            if color == 'w':
                if new_y - old_y == -1:
                    if new_y == 0:
                        return [True, True]
                    return True
                if new_y - old_y == -2 and old_y == 6:
                    return True
            if color == 'b':
                if new_y - old_y == 1:
                    if new_y == 7:
                        return [True, True]
                    return True
                if new_y - old_y == 2 and old_y == 1:
                    return True

    if abs(new_x - old_x) == 1:
        if color == 'w':
            if new_y - old_y == -1:
                if board.board[new_y][new_x]:
                    if new_y == 0:
                        return [True, True]
                    return True
        if color == 'b':
            if new_y - old_y == 1:
                if board.board[new_y][new_x]:
                    if new_y == 7:
                        return [True, True]
                    return True
    
    return False

def is_legal(board, old_x, old_y, new_x, new_y, check=False):

    piece = board.board[old_y][old_x].type

    if not check_same(board, old_x, old_y, new_x, new_y):
        return False
    
    if piece == 'q':
        if not check_bishop(board, old_x, old_y, new_x, new_y) and not check_rook(board, old_x, old_y, new_x, new_y):
            return False
    
    if piece == 'b':
        if not check_bishop(board, old_x, old_y, new_x, new_y):
            return False
    
    if piece == 'r':
        if not check_rook(board, old_x, old_y, new_x, new_y): return False
    
    if piece == 'k':
        if not check_king(board, old_x, old_y, new_x, new_y): return False
    
    if piece == 'n':
        if not check_knight(old_x, old_y, new_x, new_y): return False
    
    promote = False
    if piece == 'p':
        if isinstance(check_pawn(board, old_x, old_y, new_x, new_y), list):
            promote = True
        if not check_pawn(board, old_x, old_y, new_x, new_y):
            return False
    
    if not check_capture(board, old_x, old_y, new_x, new_y):
        return False

    if not check and not check_turn(board, old_x, old_y):
        return False

    if not check and not check_check(board, old_x, old_y, new_x, new_y):
        return False
    
    if promote:
        return [True, True]
    
    return True

def move(board, old_x, old_y, new_x, new_y):

    legal = is_legal(board, old_x, old_y, new_x, new_y)
        
    piece = board.board[old_y][old_x].type
    color = board.board[old_y][old_x].color

    if legal:
            
        if isinstance(legal, list):
            color = board.turn
            board.board[new_y][new_x] = Piece(color, 'q')

        else:
            board.board[new_y][new_x] = board.board[old_y][old_x]

        if piece == 'k' and board.turn == 'w':
            board.castle_wk, board.castle_wq = False, False
        elif piece == 'k' and board.turn == 'q':
            board.castle_bk, board.castle_bq = False, False

        board.board[old_y][old_x] = None

        board.change_turn()