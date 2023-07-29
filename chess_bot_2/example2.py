import chess.polyglot
import chess

board = chess.Board()
#opening book
book = chess.polyglot.open_reader("bookfish.bin")
move_num = 0
moves = ''

if (len(list(book.find_all(board))) != 0):
    if board.turn == chess.WHITE:
      move_num += 1
      book_move = book.weighted_choice(board).move
      moves = moves + " "+str(move_num) + ". "+str(book_move)
    else:
      book_move = book.weighted_choice(board).move
      moves = moves +" "+ str(book_move) + " "		
    print(moves)
    board.push(book_move)
    print(board)