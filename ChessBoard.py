import shelve


class BoardConfig:
    # Sample key for a grid square: "c-7"
    #                       "row_index-column_index"
    """"""
    def __init__(self, *,
                 row_len: int = 8,
                 column_len: int = 8,
                 row_letters: str = 'a-b-c-d-e-f-g-h',
                 column_letters:str = '1-2-3-4-5-6-7-8'):
        """
        Creates settings for creating instances of ChessBoard for sessions, both players share a common board

        Args:
            - board_size (int): sets the horizontal and vertical length. standart value is 8, max is 26
            - row_letters and column_letters (str): '-' is the sep, letters kit for naming sidelanes in chess board.
        """
        # checking that enought letters for lines
        assert (len(row_letters.split('-')) == column_len
                and
                len(column_letters.split('d-')) == row_len), 'not enough letters for rows or columns'
        
        # checking that no one line is longer, than 26
        assert 2 <= max(row_len, column_len) <= 26, 'board legnth more, than 26'
        
        self.row_len = row_len
        self.column_len = column_len
        self.row_letters = row_letters.split('-')
        self.column_letters = row_letters.split('-')

class Board:
    """"
    Creates an instance of board with chess pieces in initial, positions using instance of BoardConfig class
    """
    def __init__(self, BoardConfig_instance, init_positions):
        self.grid = dict()
        self.init_positions = dict()
        
        """Reads config file to find out inital positions and which squares contains which pieces"""
        with shelve.open(init_positions, 'r') as file:
            for key, value in file.items():
                self.init_positions[key] = value
        
        """Creates full chess board"""
        for row_index, column_index in (BoardConfig_instance.self.row_letters,
                                        BoardConfig_instance.self.column_letters):
            key = f"{row_index}-{column_index}"
            self.grid[key] = None
        
        """Reaplces the empty squares with pieces"""
        self.grid.update(init_positions)
    
    @staticmethod
    def set_piece(file, row_index, column_index, value):
        key = f"{row_index}-{column_index}"
        file[key] = value


def Initial_positions(BoardConfig_instance, file_name, *args: tuple[str | None, str | None, type]) -> str:
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
    with shelve.open(f'{file_name}.txt', 'n') as file:
        for arg in args:
            # cheking whether the piece class in tuple
            assert arg[2], f'func recieved arg {arg} without a piece class'
            
            # checking that at least one coordinate given
            assert arg[0] or arg[1], 'at least one coordinate must be given'
            
            
            piece_class = arg[2]
            
            # fill the entire row
            if not arg[0]:
                for row_index in BoardConfig_instance.row_letters:
                    Board.set_piece(file, row_index, arg[1], piece_class())
            
            # fill the entire column
            elif not arg[1]:
                for column_index in BoardConfig_instance.column_letters:
                    Board.set_piece(file, arg[0], column_index, piece_class())
                    
            # fill the one square
            else:
                Board.set_piece(file, arg[0], arg[1], piece_class())