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
        for usages, modes in self.starting_remaining_modes_usages.items():
            self.remaining_modes_usages[usages] = modes.copy()
        
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
        
        # this cycle find key what we need and stoping, but the key var (usages_left) leaves accessible
        for usages_left in remaining_usages:
            if mode in remaining_usages[usages_left]:
                break
        
        remaining_usages[usages_left].remove(mode)
                
        if not remaining_usages.get(usages_left-1):
            remaining_usages[usages_left-1] = []
        
        remaining_usages[usages_left-1].append(mode)