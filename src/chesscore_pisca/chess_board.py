import shelve


class BoardConfig:
    """"""
    def __init__(self, *,
                 row_len: int = 8,
                 column_len: int = 8,
                 row_letters: str = 'a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z',
                 column_letters: str = '1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26'):
        """
        Creates settings for creating instances of ChessBoard for sessions, both players share a common board

        Args:
            - board_size (int): sets the horizontal and vertical length. standart value is 8, max is 26
            - row_letters and column_letters (str): '-' is the sep, letters kit for naming sidelanes in chess board.
        """
        # checking that enought letters for lines
        assert (len(row_letters.split('-')) >= row_len
                and
                len(column_letters.split('-')) >= column_len), 'not enough letters for rows or columns'
        
        # checking that no one line is longer, than 26
        assert max(row_len, column_len) >= 2, 'both lenghts lesser, than 2'
        assert max(row_len, column_len) <= 26, 'the lenght of some side more, than 26'
        
        self.row_len = row_len
        self.column_len = column_len
        self.row_letters = row_letters.split('-')[:row_len]
        self.column_letters = column_letters.split('-')[:column_len]

class Board:
    # The sample of key for a grid square: "c-7"
    #                       "row_index-column_index"
    # The sample of value that return myboard[key]: (piece, w)
    #                                             pice instance, color
    """"
    Creates an instance of board with chess pieces in initial, positions using instance of BoardConfig class
    """
    def __init__(self, board_config, init_positions_config=None):
        self.board_config = board_config
        self.grid = dict()
        self.discarded_pieces = dict()
        
        """Reads config file to find out inital positions and which squares contains which pieces"""
        init_positions = dict()
        if init_positions_config:
            with shelve.open(init_positions_config, 'r') as db:
                for key, value in db.items():
                    init_positions[key] = value
        
        """Creates full chess board with pices from the inital_positions file"""
        color_switcher = True
        for column_index in board_config.column_letters[::-1]:
            for row_index in board_config.row_letters:
                key = f"{row_index}-{column_index}"
                color = 'w' if color_switcher else 'b'
                piece = init_positions.get(key, False)
                if piece:
                    self.grid[key] = {'piece': piece(), 'color': color}
                else:
                    self.grid[key] = {'piece': None, 'color': color}
                color_switcher = not color_switcher
            if self.board_config.row_len % 2 == 0:
                color_switcher = not color_switcher
        
        #
        for position in (f"{row_index}-{column_index}" for row_index in board_config.row_letters
                                                 for column_index in board_config.column_letters):
            if (piece := self.grid[position]['piece']) != None:
                piece.charge(self, position)
    
    def __repr__(self) -> str: #1000 repeats = 0.1600 avg seconds
        """
        !!! позже реализовать нормальный return без всего говна с форами, который будет выводить
        в правильно порядке за счет создания ключей форматированием f"x-y"
        выводить будет принтом по 1 штуке за раз!!! (наверн)
        мейби сделать генератором
        """
        rows = dict()
        
        #
        for column_index in self.board_config.column_letters:
            rows[column_index] = dict()
            
        #
        for square_coordinates, square in self.grid.items():
            square_coordinates = square_coordinates.split('-')
            column_index = square_coordinates[1]
            row_index = square_coordinates[0]
            rows[column_index][row_index] = square
        
        #
        boardstr = ''
        for row in self.board_config.column_letters[::-1]:
            for row_index in self.board_config.row_letters:
                if rows[row][row_index]['color'] == 'w':
                    naked_square = '▫'
                else:
                    naked_square = '▪'
                
                if piece:=rows[row][row_index]['piece']:
                    boardstr += f"{piece}"
                else:
                    boardstr += naked_square
                boardstr += "    "
            #
            boardstr += '\n\n'
        return boardstr.rstrip()
    
    
    def move_piece(self, old_position: str, new_position: str) -> None:
        def possible(piece, new_position):
            for usages_left in sorted(piece.remaining_modes_usages, reverse=True)[:-1]:
                for mode in piece.remaining_modes_usages[usages_left]:
                    if new_position in piece.laplace_demon[mode]:
                        return mode
                    else:
                        continue
            else:
                return False
        
        
        assert old_position in self.grid, "the try to move a unexisting square"
        assert new_position in self.grid, "the try to move on a unexisting square"
        assert self.grid[old_position]['piece'] != None, "there no piece in this square"
        assert (possible_via := possible(self.grid[old_position]['piece'], new_position)), "this piece can't make such a move"
        
        
        new = self.grid[new_position]
        old = self.grid[old_position]
        
        
        # adds the piece to self.discareded_pieces if it's will be eaten
        if new['piece'] != None:
            if new['piece'] not in self.discarded_pieces:
                self.discarded_pieces[new['piece']] = 1
            else:
                self.discarded_pieces[new['piece']] += 1
        
        self.grid[new_position]['piece'] = old['piece']
        self.grid[old_position]['piece'] = None
        self.grid[new_position]['piece'].decrease_remaining_usages(possible_via)
        self.grid[new_position]['piece'].charge(self, new_position)


def initial_positions(
    board_config,
    file_name: str = 'default_chess',
    *args: tuple[str | None, str | None, type]
) -> str:
    """
    func for setting pieces start positions, returns config for init the "Board class"
    recieves unlimited str args
    with this func you can create |, — lines with choosen pieces.
    If you set only one coordinate, then func will fill the entire line of the other coordinate with same pieces.
    
    Args:
        - a tuple containins:
            - first str: row index
            - second str: column index
            - type: the chess piece class
    
    Returns:
        - str: the path to a config file, that tells to the "Board" class how it should fill grid.
    """
    def set_piece(file, row_index, column_index, value):
        key = f"{row_index}-{column_index}"
        file[key] = value
    

    with shelve.open(file_name, 'n') as file:
        for arg in args:
            # cheking whether the piece class in tuple
            assert arg[2], f'func recieved arg without a piece class'
            # checking that at least one coordinate given
            assert arg[0] or arg[1], 'at least one coordinate must be given'
            # checking that such an index exist in the board_config
            if arg[0]:
                assert (arg[0] in board_config.row_letters), \
                f"{arg[0]} is not in the board_config row_letters"
            if arg[1]:
                assert (arg[1] in board_config.column_letters), \
                f"{arg[1]} is not in the board_config column_letters"
            
            piece_class = arg[2]
            
            # fill the entire row
            if not arg[0]:
                for row_index in board_config.row_letters:
                    set_piece(file, row_index, arg[1], piece_class)
            
            # fill the entire column
            elif not arg[1]:
                for column_index in board_config.column_letters:
                    set_piece(file, arg[0], column_index, piece_class)
                    
            # fill the one square
            else:
                set_piece(file, arg[0], arg[1], piece_class)