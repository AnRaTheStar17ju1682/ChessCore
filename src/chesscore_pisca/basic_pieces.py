from chesscore_pisca.pieces.pawn import Pawn
from chesscore_pisca.pieces.knight import Knight
from chesscore_pisca.pieces.rook import Rook
from chesscore_pisca.pieces.bishop import Bishop
from chesscore_pisca.pieces.queen import Queen


if __name__ == '__main__':
    piece_classes = tuple(name for name in globals() if not name.startswith('__'))
    from chesscore_pisca.display_moves import fast_display_piece_moves
    for piece_class in piece_classes:
        fast_display_piece_moves(globals()[piece_class])