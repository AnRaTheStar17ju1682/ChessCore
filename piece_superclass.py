class Piece:
    # key = usages left, value = movement mode
    starting_remaining_modes_usages = {float('inf'): []}
    ico = '◎'
    
    def __init__(self):
        self.laplace_demon = dict()
        self.remaining_modes_usages = dict()
        self.remaining_modes_usages[0] = []
        
        # creates copy of "starting_remaining_modes_usages"
        # where lists of modes not the same, but objs in this lists refer to the same instances
        for remaining_usages, modes in self.starting_remaining_modes_usages.items():
            self.remaining_modes_usages[remaining_usages] = modes.copy()
        
    def __repr__(self):
        return self.ico
    
    # updates the piece lapalce_demon
    def charge(self, board, position):
        # deletes old possible moves
        for modes in self.starting_remaining_modes_usages.values():
            for mode in modes:
                self.laplace_demon[mode] = []
        
        for key in self.remaining_modes_usages.keys():
            if key > 0:
                for mode in self.remaining_modes_usages[key]:
                    # the mode() returns an iterable object with positions
                    for possible_move in mode(board, position):
                        #
                        if type(possible_move) == str:
                            self.laplace_demon[mode].append(possible_move)
                        else:
                            self.laplace_demon[mode].extend(possible_move)
            else:
                continue
    
    def decrease_remaining_usages(self, mode):
        remaining_usages = self.remaining_modes_usages
        
        for usages_left in remaining_usages:
            if mode in remaining_usages[usages_left]:
                break
        
        remaining_usages[usages_left].remove(mode)
                
        if not remaining_usages.get(usages_left-1):
            remaining_usages[usages_left-1] = []
        
        remaining_usages[usages_left-1].append(mode)


if __name__ == '__main__':
    import chess_board, movement_superclass
    
    
    class my_cool_piece(Piece):
        ico = '▦'
        starting_remaining_modes_usages = {float('inf'): [movement_superclass.MovementModes(1)]}
    
    
    config = chess_board.BoardConfig(row_len=3, column_len=3)
    positions_coordinates = ((None, '1', my_cool_piece),
                             (None, '3', my_cool_piece))
    positions = chess_board.initial_positions(config, 'default_chess', *positions_coordinates)
    my_board = chess_board.Board(config, 'default_chess')
    
    print(my_board)
    my_board.move_piece('a-1', 'a-2')
    print('----------------', end='\n\n')
    print(my_board)