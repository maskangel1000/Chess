from Piece import Piece

class Board():

    def __init__(self):
        self.board = [[None for col in range(0, 8)] for row in range(0, 8)]
        
        self.board[0] = [Piece('b', 'r'), Piece('b', 'n'), Piece('b', 'b'), Piece('b', 'q'), Piece('b', 'k'), Piece('b', 'b'), Piece('b', 'n'), Piece('b', 'r')]
        self.board[1] = [Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p'), Piece('b', 'p')]

        self.board[6] = [Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p'), Piece('w', 'p')]
        self.board[7] = [Piece('w', 'r'), Piece('w', 'n'), Piece('w', 'b'), Piece('w', 'q'), Piece('w', 'k'), Piece('w', 'b'), Piece('w', 'n'), Piece('w', 'r')]

        self.turn = 'w'
    
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