from chesscore_pisca.piece_superclass import Piece
from chesscore_pisca.basic_movement import KnightMovement


class Knight(Piece):
    knight_movement = KnightMovement()
    starting_remaining_modes_usages = {float('inf'): [knight_movement]}
    ico = '♘'


if __name__ == '__main__':
    from chesscore_pisca.display_moves import fast_display_piece_moves
    fast_display_piece_moves(Knight)