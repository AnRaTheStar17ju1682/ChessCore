from chesscore_pisca.piece_superclass import Piece
from chesscore_pisca.basic_movement import TopRight, TopLeft, BottomRight, BottomLeft


class Bishop(Piece):
    top_right = TopRight()
    top_left = TopLeft()
    bottom_right = BottomRight()
    bottom_left = BottomLeft()
    
    starting_remaining_modes_usages = {float('inf'): [top_right, top_left, bottom_right, bottom_left]}
    ico = '♗'


if __name__ == '__main__':
    from chesscore_pisca.display_moves import fast_display_piece_moves
    fast_display_piece_moves(Bishop)