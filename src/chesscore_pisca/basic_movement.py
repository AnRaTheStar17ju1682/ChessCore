from chesscore_pisca.movement_superclass import MovementMode, JumpMovementMode


class Forward(MovementMode):
    def func(self, board, position):
        return self.move(board, position, column=True)
    

class Backward(MovementMode):
    def func(self, board, position):
        return self.move(board, position, column=True, offset=-1)


class Rightward(MovementMode):
    def func(self, board, position):
        return self.move(board, position, row=True, offset=1)


class Leftward(MovementMode):
    def func(self, board, position):
        return self.move(board, position, row=True, offset=-1)


class TopRight(MovementMode):
    def func(self, board, position):
        vposition = self.move(board, position, column=True, offset=1)
        vposition = self.move(board, vposition, row=True, offset=1)
        return vposition


class TopLeft(MovementMode):
    def func(self, board, position):
        vposition = self.move(board, position, column=True, offset=1)
        vposition = self.move(board, vposition, row=True, offset=-1)
        return vposition


class BottomRight(MovementMode):
    def func(self, board, position):
        vposition = self.move(board, position, column=True, offset=-1)
        vposition = self.move(board, vposition, row=True, offset=1)
        return vposition


class BottomLeft(MovementMode):
    def func(self, board, position):
        vposition = self.move(board, position, column=True, offset=-1)
        vposition = self.move(board, vposition, row=True, offset=-1)
        return vposition


class KnightMovement(JumpMovementMode):
    path_data = ({'path': '+x +x +y', 'smash': True, 'active_sectors': 'all'}, 'END')