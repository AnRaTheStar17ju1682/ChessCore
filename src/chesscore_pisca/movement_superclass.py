class MovementMode:
    def func(self, board, position):
        return board.grid.keys()
    
    
    def __init__(self, max_iterations = float('inf')):
        self.max_iterations = max_iterations
    
    
    def __call__(self, board, position):
        iteration = 0
        vposition = position
        
        while iteration < self.max_iterations:
            # will repeates untill reaching max_iterations or end of grid
            try:
                vposition = self.func(board, vposition)
            except IndexError:
                break
            
            iteration += 1
            
            # че если вернется несколько в одной?
            if board.grid[vposition]['piece']:
                yield vposition
                break
            else:
                yield vposition
    
    
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


class JumpMovementMode(MovementMode):
    path_data = ({'path': '+y +y +x', 'smash': True, 'sectors': 'all'}, 'END')
    
    
    def __init__(self):
        super().__init__(self)
    
    
    def __call__(self, board, position):
        def generate_rotated_paths(
                position,
                path_data,
                current_sector='+y+x',
                relativity=('+y+x', '+y-x', '-x+y', '-x-y', '-y-x', '-y+x', '+x-y', '+x+y')
            ):
            # exit condition
            if path_data[0] == 'END':
                return []
            
            
            path = path_data[0]['path']
            smash = path_data[0]['smash']
            active_sectors = path_data[0]['sectors']
            smash_list = list()
            # это нужно для первой итерации
            old_sector = current_sector


            index = relativity.index(current_sector)
            relativity = relativity[index:] + relativity[:index]
            
            
            for current_sector in relativity:
                vposition = position
                
                
                # блок обработки пути для нового сектора
                main = current_sector[:2]
                sub = current_sector[2:]
                old_main = old_sector[:2]
                old_sub = old_sector[2:]
                
                if main[1] != old_main[1]:
                    trans_table = path.maketrans('xy', 'yx')
                    path = path.translate(trans_table)
                
                for current, old in (main, old_main), (sub, old_sub):
                    if current[0] != old[0]:
                        axis = current[1]
                        path = path.replace(f'-{axis}', f'*{axis}')
                        path = path.replace(f'+{axis}', f'-{axis}')
                        path = path.replace(f'*{axis}', f'+{axis}')
                
                
                # само выполнение уже измененного пути
                commands = path.split(' ')
                for command in commands:
                    sign = command[0]
                    offset = sign + '1'
                    offset = int(offset)
                    if command[1] == 'x':
                        vposition = self.move(board, vposition, row=True, offset=offset)
                    else:
                        vposition = self.move(board, vposition, column=True, offset=offset)
                
                
                # если сам промежуточный путь тоже должен бить при ходьбе
                if smash:
                    smash_list += [vposition]
                # дальнейшее развитие пути и внесение дочерних путей в смэшлист
                smash_list += generate_rotated_paths(vposition, path_data[1:], current_sector=current_sector)
                # нужно для корректной модификации пути
                old_sector = current_sector
            
            return smash_list
        

        for possible_move in generate_rotated_paths(position, self.path_data):
            if board.grid[possible_move]['piece']:
                yield possible_move
                continue
            else:
                yield possible_move