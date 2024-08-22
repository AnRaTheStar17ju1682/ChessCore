import movement_superclass


class PawnDoubleMove(movement_superclass):
    def __init__(self):
        super().__init__(max_iterations = 1)
    
    def func(self, board, position):
        new_position = self.move(board, position, column = True, offset=2)
        return new_position