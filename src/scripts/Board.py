from Piece import Piece

class Board:

    PIECE_TYPE = {
        'k' : 'bk',
        'K' : 'wk',
        'q' : 'bq',
        'Q' : 'wq',
        'b' : 'bb',
        'B' : 'wb',
        'r' : 'br',
        'R' : 'wr',
        'n' : 'bn',
        'N' : 'wn',
        'p' : 'bp',
        'P' : 'wp'
    }

    LETTERS_COLUMNS = {
        'a' : 0,
        'b' : 1,
        'c' : 2,
        'd' : 3,
        'e' : 4,
        'f' : 5,
        'g' : 6,
        'h' : 7
    }

    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self):
        self.reset_board()
        self.current_fen = 0
        self.fen_list = [Board.START_FEN]

    def reset_board(self):
        self.board = [[None for col in range(0, 8)] for row in range(0, 8)]
        self.load_fen(Board.START_FEN)
    
    def load_fen(self, fen):

        fen_board = fen.split(" ")[0]
        file = 0
        rank = 0

        for char in fen_board:
            if char == "/":
                file = 0
                rank += 1
            else:
                if char.isdigit():
                    for i in range(file, file+int(char)):
                        self.board[rank][i] = None
                    file += int(char)
                else:
                    piece = Board.PIECE_TYPE[char]
                    self.board[rank][file] = Piece(piece[0], piece[1], rank, file)
                    file += 1
        
        self.turn = fen.split(" ")[1]

        self.castle_wk = True if "K" in fen.split(" ")[2] else False
        self.castle_wq = True if "Q" in fen.split(" ")[2] else False
        self.castle_bk = True if "k" in fen.split(" ")[2] else False
        self.castle_bq = True if "q" in fen.split(" ")[2] else False

        self.enpassant_x = Board.LETTERS_COLUMNS[fen.split(" ")[3][0]] if fen.split(" ")[3] != "-" else None
        self.enpassant_y = 8 - int(fen.split(" ")[3][1]) if fen.split(" ")[3] != "-" else None

        self.half_moves = fen.split(" ")[4]
        self.full_moves = fen.split(" ")[5]
    
    """rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    / - next rank
    digit - blank spaces until next piece
    kK/bW - piece types

    w/b - turn

    KQkq - black/white able to castle"""
    def position_to_fen(self) -> str:
        fen = ""
        for row in self.board:
            digit = 0
            hold_digit = 0
            for piece in row:
                if piece == None:
                    digit += 1
                else:
                    if digit > 0 and digit != hold_digit:
                        hold_digit = digit
                        fen += str(digit)
                    piece_name = {i for i in Board.PIECE_TYPE if Board.PIECE_TYPE[i] == f"{piece.color}{piece.type}"}
                    fen += str(list(piece_name)[0])
                    digit = 0
                    hold_digit = 0
            if digit > 0 and digit != hold_digit:
                fen += str(digit)
            fen += "/"
        fen = fen[:-1]
        fen += f" {self.turn} "
        
        fen += "K" if self.castle_wk else ""
        fen += "Q" if self.castle_wq else ""
        fen += "k" if self.castle_bk else ""
        fen += "q" if self.castle_bq else ""
        
        fen += f" - {self.half_moves} {self.full_moves}"
        
        return fen
    
    def change_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'
    
    def to_string(self):
        board_string = """"""
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                piece = self.board[row][col]
                if piece:
                    board_string += piece.to_string() + " "
                else:
                    board_string += "xx "
            board_string += "\n"
        return board_string
