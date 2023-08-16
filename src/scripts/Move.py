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

def is_checkmate(board):
    for row in range(0, len(board.board)):
        for col in range(0, len(board.board[row])):
            piece = board.board[row][col]
            if piece and piece.color == board.turn:
                for row2 in range(0, len(board.board)):
                    for col2 in range(0, len(board.board)):
                        if is_legal(board, col, row, col2, row2):
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
    
    if board.turn == 'w':
        if board.castle_wk and new_x == 6 and new_y == 7:
            if not board.board[7][5] and not board.board[7][6]:
                if board.board[7][7] and board.board[7][7].color == 'w' and board.board[7][7].type == 'r':
                    return [True, True]
        if board.castle_wq and new_x == 2 and new_y == 7:
            if not board.board[7][1] and not board.board[7][2] and not board.board[7][3]:
                if board.board[7][0] and board.board[7][0].color == 'w' and board.board[7][0].type == 'r':
                    return [True, True]
    if board.turn == 'b':
        if board.castle_bk and new_x == 6 and new_y == 0:
            if not board.board[0][5] and not board.board[0][6]:
                if board.board[0][7] and board.board[0][7].color == 'b' and board.board[0][7].type == 'r':
                    return [True, True]
        if board.castle_bq and new_x == 2 and new_y == 0:
            if not board.board[0][1] and not board.board[0][2] and not board.board[0][3]:
                if board.board[0][0] and board.board[0][0].color == 'b' and board.board[0][0].type == 'r':
                    return [True, True]
    
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
                        return [True, 1]
                    return True
                if new_y - old_y == -2 and old_y == 6:
                    if not board.board[old_y-1][old_x]:
                        return [True, 3, new_x, new_y+1]
            if color == 'b':
                if new_y - old_y == 1:
                    if new_y == 7:
                        return [True, 1]
                    return True
                if new_y - old_y == 2 and old_y == 1:
                    if not board.board[old_y+1][old_x]:
                        return [True, 3, new_x, new_y-1]

    if abs(new_x - old_x) == 1:
        if color == 'w':
            if new_y - old_y == -1:
                if board.board[new_y][new_x]:
                    if new_y == 0:
                        return [True, 1]
                    return True
                elif board.enpassant_x == new_x and board.enpassant_y == new_y:
                    return [True, 2]
        if color == 'b':
            if new_y - old_y == 1:
                if board.board[new_y][new_x]:
                    if new_y == 7:
                        return [True, 1]
                    return True
                elif board.enpassant_x == new_x and board.enpassant_y == new_y:
                    return [True, 2]
    
    return False

def is_legal(board, old_x, old_y, new_x, new_y, check=False):

    piece = board.board[old_y][old_x].type

    if not check and not check_same(board, old_x, old_y, new_x, new_y):
        return False
    
    if piece == 'q':
        if not check_bishop(board, old_x, old_y, new_x, new_y) and not check_rook(board, old_x, old_y, new_x, new_y):
            return False
    
    if piece == 'b':
        if not check_bishop(board, old_x, old_y, new_x, new_y):
            return False
    
    if piece == 'r':
        if not check_rook(board, old_x, old_y, new_x, new_y): return False
    
    castle = False
    if piece == 'k':
        if isinstance(check_king(board, old_x, old_y, new_x, new_y), list):
            castle = True
        if not check_king(board, old_x, old_y, new_x, new_y):
            return False
    
    if piece == 'n':
        if not check_knight(old_x, old_y, new_x, new_y): return False
    
    promote = False
    enpassant = False
    keep_enpassant = False
    if piece == 'p':
        return_list = check_pawn(board, old_x, old_y, new_x, new_y)
        if isinstance(return_list, list):
            if return_list[1] == 1:
                promote = True
            elif return_list[1] == 2:
                enpassant = True
            elif return_list[1] == 3:
                keep_enpassant = [True, 4, return_list[2], return_list[3]]
        if not check_pawn(board, old_x, old_y, new_x, new_y):
            return False
    
    if not check_capture(board, old_x, old_y, new_x, new_y):
        return False

    if not check and not check_turn(board, old_x, old_y):
        return False

    if not check and not check_check(board, old_x, old_y, new_x, new_y):
        return False
    
    if promote:
        return [True, 1]
    
    if castle:
        return [True, 2]
    
    if enpassant:
        return [True, 3]
    
    if keep_enpassant:
        return keep_enpassant
    
    return True

def move(board, old_x, old_y, new_x, new_y):

    legal = is_legal(board, old_x, old_y, new_x, new_y)
        
    piece = board.board[old_y][old_x].type
    color = board.turn

    if legal:
        if isinstance(legal, list):
            if legal[1] == 1: # Promote
                board.board[new_y][new_x] = Piece(color, 'q', new_y, new_x)
            elif legal[1] == 2: # Castle
                if color == 'w' and new_x == 6:
                    board.board[new_y][new_x] = Piece(color, 'k', new_y, new_x)
                    board.board[new_y][new_x-1] = Piece(color, 'r', new_y, new_x)
                    board.board[new_y][7] = None
                elif color == 'w' and new_x == 2:
                    board.board[new_y][new_x] = Piece(color, 'k', new_y, new_x)
                    board.board[new_y][new_x+1] = Piece(color, 'r', new_y, new_x)
                    board.board[new_y][0] = None
                elif color == 'b' and new_x == 6:
                    board.board[new_y][new_x] = Piece(color, 'k', new_y, new_x)
                    board.board[new_y][new_x-1] = Piece(color, 'r', new_y, new_x)
                    board.board[new_y][7] = None
                elif color == 'b' and new_x == 2:
                    board.board[new_y][new_x] = Piece(color, 'k', new_y, new_x)
                    board.board[new_y][new_x+1] = Piece(color, 'r', new_y, new_x)
                    board.board[new_y][0] = None
            elif legal[1] == 3: # Enpassant
                board.board[new_y][new_x] = board.board[old_y][old_x]
                if color == 'w':
                    board.board[new_y+1][new_x] = None
                else:
                    board.board[new_y-1][new_x] = None
            elif legal[1] == 4: # Keep enpassant
                board.enpassant_x = legal[2]
                board.enpassant_y = legal[3]
                board.board[new_y][new_x] = board.board[old_y][old_x]
        else:
            board.board[new_y][new_x] = board.board[old_y][old_x]

        # Castling
        # TODO: If rook is taken before moving, then other rook is placed in its spot, player can still castle
        
        if piece != 'p' or not isinstance(legal, list) or (isinstance(legal, list) and legal[1] != 4):
            board.enpassant_x, board.enpassant_y = None, None

        if piece == 'k' and board.turn == 'w':
            board.castle_wk, board.castle_wq = False, False
        elif piece == 'k' and board.turn == 'q':
            board.castle_bk, board.castle_bq = False, False
        
        elif piece == 'r' and board.turn == 'w':
            if old_y == 7 and old_x == 7:
                board.castle_wk = False
            if old_y == 7 and old_x == 0:
                board.castle_wq = False
        elif piece == 'r' and board.turn == 'b':
            if old_y == 0 and old_x == 7:
                board.castle_bk = False
            if old_y == 0 and old_x == 0:
                board.castle_bq = False

        board.board[old_y][old_x] = None

        board.change_turn()

        return True
    
    return False