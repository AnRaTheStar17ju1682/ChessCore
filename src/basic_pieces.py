import piece_superclass

class Pawn(piece_superclass.Piece):
    modes_usages = {1: piece_superclass.movement.PawnDoubleMove()}
    ico = '♙'