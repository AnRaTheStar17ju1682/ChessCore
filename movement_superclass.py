class MovementModes:
    def func(self, board, position):
        return board.grid.keys()
    
    def __init__(self, max_iterations = float('inf')):
        self.max_iterations = max_iterations
    
    def __call__(self, board, position):
        def iterable(self):
            iteration = 0
            
            while iteration < self.max_iterations:
                # will repeates untill reaching max_iterations or end of grid
                try:
                    new_move = self.func(board, position)
                except IndexError:
                    raise StopIteration
                iteration += 1
                yield new_move
            
        return iterable(self)
    
    def move(self, board, position, *,
                    row: bool = False,
                    column: bool = False,
                    offset = 1):
        assert row or column, 'at least one must be chosen'
        
        edges = (row := 'row' if row else '',
                 column := 'column' if column else '')

        current_position = position.split('-')
        new_position = list()
        
        for edge, current_letter in zip(edges, current_position):
            if edge:
                letters = getattr(board.board_config, f"{edge}_letters")
                index = letters.index(current_letter)
                new_letter = letters[index + offset]   
            else:
                new_letter = current_letter
            new_position.append(new_letter)

        return '-'.join(new_position)