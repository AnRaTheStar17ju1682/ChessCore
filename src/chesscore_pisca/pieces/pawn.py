from chesscore_pisca.piece_superclass import Piece
from chesscore_pisca.basic_movement import Forward


class PawnSingleForward(Forward):
    def __init__(self, max_iterations=1):
        super().__init__(max_iterations)


class PawnDoubleForward(Forward):
    def __init__(self, max_iterations=2):
        super().__init__(max_iterations)


class Pawn(Piece):
    single_forward = PawnSingleForward()
    double_forward = PawnDoubleForward()
    starting_remaining_modes_usages = {float('inf'): [single_forward], 1: [double_forward]}
    first_step_only = [double_forward]
    ico = '♙'


if __name__ == '__main__':
    from chesscore_pisca.display_moves import fast_display_piece_moves
    fast_display_piece_moves(Pawn, then_move='e-7')