import chess as ch
import chess.polyglot
import random as rd
import time

class Engine:

    def __init__(self, board, maxDepth, color):
        self.board=board
        self.color=color
        self.maxDepth=maxDepth
        self.book = chess.polyglot.open_reader("C:/Users/jacop/Prove/projects/chess_bot_2/bookfish.bin")

        self.material = {
            chess.PAWN:10.0,
	        chess.KNIGHT:30.5,
	        chess.BISHOP:35.0,
	        chess.ROOK:54.8,
	        chess.QUEEN:94.8,
            chess.KING:200.0
        }

        self.scoring = {
            'Pawn': [
                0, 0, 0, 0, 0, 0, 0, 0, 
                5, 5, 5, 5, 5, 5, 5, 5, 
                1, 1, 2, 3, 3, 2, 1, 1, 
                0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5, 
                0, 0, 0, 2, 2, 0, 0, 0, 
                0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
                0.5, 1, 1, -2, -2, 1, 1, 0.5, 
                0, 0, 0, 0, 0, 0, 0, 0],
            'Knight': [
                -5, -4, -3, -3, -3, -3, -4, -5,
                -4, -2, 0, 0, 0, 0, -2, -4, 
                -3, 0, 1, 1.5, 1.5, 1, 0, -3, 
                -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3, 
                -3, 0, 1.5, 2, 2, 1.5, 0, -3,
                -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3, 
                -4, -2, 0, 0.5, 0.5, 0, -2, -4, 
                -5, -4, -3, -3, -3, -3, -4, -5],
            'Bishop': [
                -2, -1, -1, -1, -1, -1, -1, -2,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0.5, 1, 1, 0.5, 0, -1,
                -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, 
                -1, 0, 1, 1, 1, 1, 0, -1, 
                -1, 1, 1, 1, 1, 1, 1, -1, 
                1, 0.5, 0, 0, 0, 0, 0.5, -1,
                -2, -1, -1, -1, -1, -1, -1, -2],
            'Rook': [
                0, 0, 0, 0, 0, 0, 0, 0, 
                0.5, 1, 1, 1, 1, 1, 1, 0.5, 
                -0.5, 0, 0, 0, 0, 0, 0, -0.5, 
                -0.5, 0, 0, 0, 0, 0, 0, -0.5, 
                -0.5, 0, 0, 0, 0, 0, 0, -0.5, 
                -0.5, 0, 0, 0, 0, 0, 0, -0.5, 
                -0.5, 0, 0, 0, 0, 0, 0, -0.5, 
                0, 0, 0, 0.5, 0.5, 0, 0, 0],
            'Queen': [
                -2, -1, -1, -0.5, -0.5, -1, -1, -2,
                -1, 0, 0, 0, 0, 0, 0, -1, 
                -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1, 
                -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5, 
                0, 0, 0.5, 0.5, 0.5, 0, 0, -0.5, 
                -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1, 
                -1, 0, 0.5, 0.5, 0, 0, 0, -1,
                -2, -1, -1, -0.5, -0.5, -1, -1, -2],
            'King': [
                -3, -4, -4, -5, -5, -4, -4, -3, 
                -3, -4, -4, -5, -5, -4, -4, -3, 
                -3, -4, -4, -5, -5, -4, -4, -3, 
                -3, -4, -4, -5, -5, -4, -4, -3, 
                -2, -3, -3, -4, -4, -3, -3, -2, 
                -1, -2, -2, -2, -2, -2, -2, -1, 
                2, 2, 0, 0, 0, 0, 2, 2, 
                2, 3, 1, 0, 0, 1, 3, 2],
        }


        self.pawn_table = self.scoring['Pawn']
        self.knight_table = self.scoring['Knight']
        self.bishop_table = self.scoring['Bishop']
        self.rook_table = self.scoring['Rook']
        self.queen_table = self.scoring['Queen']
        self.king_table = self.scoring['King']
    
    def getBestMove(self):
        return self.engine(None, 1)
    
    def mobility(self, board):
        current = board.turn
        board.turn = chess.WHITE
        white_moves = len(list(board.legal_moves))
        board.turn = chess.BLACK
        black_moves = len(list(board.legal_moves))
        board.turn = current
        mobility_score = 0.4*(white_moves - black_moves)
        return mobility_score

    def evalFunct(self):
        if self.board.can_claim_draw() or self.board.is_stalemate() or self.board.is_insufficient_material():
            score = 0.00
            pst_score = 0.00
        elif self.board.is_checkmate():
            if self.board.turn == chess.BLACK:
                score = float("inf")
                pst_score = 0.00
            else:
                score = -float("inf")
                pst_score = 0.00			
        else:
            score = 0.00
            pst_score = 0.00
            pieces = self.board.piece_map()
            for square, piece in pieces.items():
                if piece.color:
                    score += self.material[piece.piece_type]
                    if piece.piece_type == chess.PAWN:
                        pst_score += self.pawn_table[square]
                    elif piece.piece_type == chess.KNIGHT:
                        pst_score += self.knight_table[square]
                    elif piece.piece_type == chess.BISHOP:
                        pst_score += self.bishop_table[square]
                    elif piece.piece_type == chess.ROOK:
                        pst_score += self.rook_table[square]
                    elif piece.piece_type == chess.QUEEN:
                        pst_score += self.queen_table[square]
                    elif piece.piece_type == chess.KING:
                        pst_score += self.king_table[square]
                else:
                    score -= self.material[piece.piece_type]
                    if piece.piece_type == chess.PAWN:
                        pst_score -= self.pawn_table[chess.square_mirror(square)]
                    elif piece.piece_type == chess.KNIGHT:
                        pst_score -= self.knight_table[chess.square_mirror(square)]
                    elif piece.piece_type == chess.BISHOP:
                        pst_score -= self.bishop_table[chess.square_mirror(square)]
                    elif piece.piece_type == chess.ROOK:
                        pst_score -= self.rook_table[chess.square_mirror(square)]
                    elif piece.piece_type == chess.QUEEN:
                        pst_score -= self.queen_table[chess.square_mirror(square)]
                    elif piece.piece_type == chess.KING:
                        pst_score -= self.king_table[chess.square_mirror(square)]
        if self.board.turn == chess.WHITE:
            pst_score += 0.4
        else:
            pst_score -=0.4
        mobility_score = self.mobility(self.board)
        pst_score += mobility_score
        return score + pst_score
    
    def alpha_beta_with_quiescence(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evalFunct()

        if maximizing_player:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.alpha_beta_with_quiescence(board, depth - 1, alpha, beta, False))
                board.pop()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.alpha_beta_with_quiescence(board, depth - 1, alpha, beta, True))
                board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return alpha if maximizing_player else beta
       
    def engine(self, candidate, depth):
        #opening book
        if (self.book.get(self.board) != None):
            if self.board.turn == chess.WHITE:
                book_move = self.book.weighted_choice(self.board).move
            else:
                book_move = self.book.weighted_choice(self.board).move
            return book_move
        else:
            start_time = time.time()
            #reached max depth of search or no possible moves
            if ( depth == self.maxDepth or self.board.legal_moves.count() == 0):
                return self.evalFunct()
            
            else:
                if self.board.turn == chess.WHITE:
                    best_value = -float("inf")
                else:
                    best_value = float("inf")
                
                #analyse board after deeper moves
                for d in range(1, self.maxDepth + 1):
                    for move in self.board.legal_moves:
                        #Play move i
                        self.board.push(move)

                        if self.board.turn == chess.WHITE:
                            value = self.alpha_beta_with_quiescence(self.board, d, float('-inf'), float('inf'), True)
                        else:
                            value = self.alpha_beta_with_quiescence(self.board, d, float('-inf'), float('inf'), True)
                        self.board.pop()
                        if self.board.turn == chess.WHITE:
                            if value > best_value:
                                best_value = value
                                best_move = move
                        else:
                            if value < best_value:
                                best_value = value
                                best_move = move
                        if time.time() - start_time >= 600:
                            #if best_move == None:
                            #    legals = list(self.board.legal_moves)
                            #    best_move = chess.Move.from_uci(rd.choice(legals))
                            return best_move
                            break
                return best_move








        
        




        




    
    
