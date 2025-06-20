import chess.pgn
import chess

board = chess.Board()
game = chess.pgn.Game()

#print(board.legal_moves)
board.legal_moves
chess.Move.from_uci("a8a1") in board.legal_moves

print("hello")
print(chess.Move.from_uci("a8a1"))


#print("fullmovenumber:", board.fullmove_number)
node = game.add_variation(board.push("e4"))
print(chess.Board.turn())
#print("fullmovenumber:", board.fullmove_number)
node = node.add_variation(node.push("d5"))
print(chess.Board.turn())
#print("fullmovenumber:", board.fullmove_number)
node = node.add_variation(node.push("exd5"))
print(chess.Board.turn())
node = node.add_variation(node.push("h5"))
print(chess.Board.turn())
print(board)




'''
board.is_checkmate()
board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
'''
