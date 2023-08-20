from Game import main
from Board import Board

if __name__ == "__main__":
    board = Board()
    print(board.position_to_fen())
    main(board)