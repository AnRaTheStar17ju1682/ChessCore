from chesscore_pisca.piece_superclass import Piece
from chesscore_pisca.basic_movement import Forward, Backward, Rightward, Leftward


class Rook(Piece):
    forward = Forward()
    backward = Backward()
    righward = Rightward()
    leftward = Leftward()
    
    starting_remaining_modes_usages = {float('inf'): [forward, backward, righward, leftward]}
    ico = '♖'


if __name__ == '__main__':
    from chesscore_pisca.display_moves import fast_display_piece_moves
    fast_display_piece_moves(Rook)