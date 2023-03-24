from Piece import Piece

class Board():

    def __init__(self):

        self.board = [[None for col in range(0, 8)] for row in range(0, 8)]

        start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.load_fen(start_fen)
    
    def load_fen(self, fen):

        piece_type = {
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

        letters_columns = {
            'a' : 0,
            'b' : 1,
            'c' : 2,
            'd' : 3,
            'e' : 4,
            'f' : 5,
            'g' : 6,
            'h' : 7
        }

        fen_board = fen.split(" ")[0]
        file = 0
        rank = 0

        for char in fen_board:
            if char == "/":
                file = 0
                rank += 1
            else:
                if char.isdigit():
                    file += int(char)
                else:
                    piece = piece_type[char]
                    self.board[rank][file] = Piece(piece[0], piece[1])
                    file += 1
        
        self.turn = fen.split(" ")[1]

        self.castle_wk = True if "K" in fen.split(" ")[2] else False
        self.castle_wq = True if "Q" in fen.split(" ")[2] else False
        self.castle_bk = True if "k" in fen.split(" ")[2] else False
        self.castle_bq = True if "q" in fen.split(" ")[2] else False

        self.enpassant_x = letters_columns[fen.split(" ")[3][0]] if fen.split(" ")[3] != "-" else None
        self.enpassant_y = 8 - int(fen.split(" ")[3][1]) if fen.split(" ")[3] != "-" else None

        self.half_moves = fen.split(" ")[4]
        self.full_moves = fen.split(" ")[5]
    
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