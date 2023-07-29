import chess
import time
import chess.polyglot
import os
import random
board = chess.Board()
book = chess.polyglot.open_reader("baron30.bin")
moves = ""
move_num = 0
material = {
  chess.PAWN:10.0,
	chess.KNIGHT:32.0,
	chess.BISHOP:33.3,
	chess.ROOK:56.5,
	chess.QUEEN:95.5,
  chess.KING:200.0
	
}
scoring = {
 'Pawn': [
  0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 2, 3, 3, 2, 1, 1, 0, 0,
  0, 2, 2, 0, 0, 0, 0, 0, 0, -2, -2, 0, 0, 0, 1, -1, -2, 0, 0, -2, -1, 1, 1, 2,
  2, -2, -2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0
 ],
 'Knight': [
  -5, -4, -3, -3, -3, -3, -4, -5, -4, -2, 0, 0, 0, 0, -2, -4, -3, 0, 1, 1.5,
  1.5, 1, 0, -3, -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3, -3, 0.5, 1.5, 2, 2, 1.5,
  0.5, -3, -3, 0, 1, 1.5, 1.5, 1, 0, -3, -4, -2, 0, 0.5, 0.5, 0, -2, -4, -5,
  -4, -3, -3, -3, -3, -4, -5
 ],
 'Bishop': [
  -2,
  -1,
  -1,
  -1,
  -1,
  -1,
  -1,
  -2,
  -1,
  0.25,
  0,
  0,
  0,
  0,
  0.25,
  -1,
  -1,
  0,
  1,
  1,
  1,
  1,
  0,
  -1,
  -1,
  0,
  1,
  1.5,
  1.5,
  1,
  0,
  -1,
  -1,
  0,
  1,
  1.5,
  1.5,
  1,
  0,
  -1,
  -1,
  0,
  1,
  1,
  1,
  1,
  0,
  -1,
  -1,
  0.25,
  0,
  0,
  0,
  0,
  0.25,
  -1,
  -2,
  -1,
  -1,
  -1,
  -1,
  -1,
  -1,
  -2,
 ],
 'Rook': [
  0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, 1, 1, 1, 1, 0.5, -0.5, 0, 0, 0, 0, 0, 0,
  -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0, 0, 0, 0, 0, -0.5, -0.5, 0, 0,
  0, 0, 0, 0, -0.5, -0.5, 1, 1, 1, 1, 1, 1, -0.5, 0, 0, 0, 0.5, 0.5, 0, 0, 0
 ],
 'Queen': [
  -2, -1, -1, -0.5, -0.5, -1, -1, -2, -1, 0, 0.5, 0, 0, 0.5, 0, -1, -1, 0.5,
  0.5, 0.5, 0.5, 0.5, 0.5, -1, -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, 0, 0, 0.5,
  0.5, 0.5, 0, 0, 0, -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, -1, 0.5, 0.5, 0.5,
  0.5, 0.5, 0.5, -1, -2, -1, -1, -0.5, -0.5, -1, -1, -2
 ],
 'King': [
  -3, -4, -4, -5, -5, -4, -4, -3, -3, -4, -4, -5, -5, -4, -4, -3, -3, -4, -4,
  -5, -5, -4, -4, -3, -3, -4, -4, -5, -5, -4, -4, -3, -2, -3, -3, -4, -4, -3,
  -3, -2, -1, -2, -2, -2, -2, -2, -2, -1, 2, 2, 0, 0, 0, 0, 2, 2, 2, 3, 1, 0,
  0, 1, 3, 2
 ],
}
pawn_table = scoring['Pawn']
knight_table = scoring['Knight']
bishop_table = scoring['Bishop']
rook_table = scoring['Rook']
queen_table = scoring['Queen']
king_table = scoring['King']

def mobility(board):
    current = board.turn
    board.turn = chess.WHITE
    white_moves = len(list(board.legal_moves))
    board.turn = chess.BLACK
    black_moves = len(list(board.legal_moves))
    board.turn = current
    mobility_score = 0.4*(white_moves - black_moves)
    return mobility_score

def evaluate(board):
  if board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
    score = 0.00
    pst_score = 0.00
  elif board.is_checkmate():
    if board.turn == chess.BLACK:
      score = float("inf")
      pst_score = 0.00
    else:
      score = -float("inf")
      pst_score = 0.00			
  else:
    score = 0.00
    pst_score = 0.00
    pieces = board.piece_map()
    for square, piece in pieces.items():
      if piece.color:
        score += material[piece.piece_type]
        if piece.piece_type == chess.PAWN:
          pst_score += pawn_table[square]
        elif piece.piece_type == chess.KNIGHT:
          pst_score += knight_table[square]
        elif piece.piece_type == chess.BISHOP:
          pst_score += bishop_table[square]
        elif piece.piece_type == chess.ROOK:
          pst_score += rook_table[square]
        elif piece.piece_type == chess.QUEEN:
          pst_score += queen_table[square]
        elif piece.piece_type == chess.KING:
          pst_score += king_table[square]
      else:
        score -= material[piece.piece_type]
        if piece.piece_type == chess.PAWN:
          pst_score -= pawn_table[chess.square_mirror(square)]
        elif piece.piece_type == chess.KNIGHT:
           pst_score -= knight_table[chess.square_mirror(square)]
        elif piece.piece_type == chess.BISHOP:
           pst_score -= bishop_table[chess.square_mirror(square)]
        elif piece.piece_type == chess.ROOK:
         pst_score -= rook_table[chess.square_mirror(square)]
        elif piece.piece_type == chess.QUEEN:
          pst_score -= queen_table[chess.square_mirror(square)]
        elif piece.piece_type == chess.KING:
          pst_score -= king_table[chess.square_mirror(square)]
  if board.turn == chess.WHITE:
    pst_score += 0.4
  else:
     pst_score -=0.4
  mobility_score = mobility(board)
  pst_score += mobility_score
  return score + pst_score

threshhold_depth = 15

def highest_value(board):
  start_time = time.time()
  best_move = None
  if board.turn == chess.WHITE:
    best_value = -float("inf")
  else:
    best_value = float("inf")
  for d in range(1, threshhold_depth + 1):
    for move in board.legal_moves:
      board.push(move)
      if board.turn == chess.WHITE:
        value = alpha_beta_with_quiescence(board, threshhold_depth, float('-inf'), float('inf'), True)
      else:
        value = alpha_beta_with_quiescence(board, threshhold_depth, float('-inf'), float('inf'), True)
      board.pop()
      if board.turn == chess.WHITE:
        if value > best_value:
          best_value = value
          best_move = move
      else:
        if value < best_value:
          best_value = value
          best_move = move
      if time.time() - start_time >= 5:
        if best_move == None:
          legals = list(board.legal_moves)
          best_move = chess.Move.from_uci(random.choice(legals))
        return best_move
        break
  return best_move

def quiescence_search(board, alpha, beta, maximizing_player):
    if board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        value = float('-inf')
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiescence_search(board, -beta, -alpha, False)
                board.pop()
                
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
    else:
        value = float('inf')
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiescence_search(board, -beta, -alpha, True)
                board.pop()

                if score <= alpha:
                    return alpha
                beta = min(beta, score)

    return alpha if maximizing_player else beta

def alpha_beta_with_quiescence(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return quiescence_search(board, alpha, beta, maximizing_player)

    if maximizing_player:
        value = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            value = max(value, alpha_beta_with_quiescence(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = min(value, alpha_beta_with_quiescence(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break

    return alpha if maximizing_player else beta

while True:
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
            time.sleep(1)
            os.system("clear")
            print(board)
    else:
        best_move = highest_value(board)
        if board.turn == chess.WHITE:
            move_num += 1
            moves = moves + " "+ str(move_num) + ". "+str(best_move)
        else:
            moves = moves + " "+str(best_move) + " "		
            board.push(best_move)
            os.system("clear")
            print(moves)
            print(board)
        if board.can_claim_draw() == True:
            print("draw")
        break
