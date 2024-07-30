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
                len(column_letters.split('-')) == row_len), 'not enough letters for rows or columns'
        
        # checking that no one line is longer, than 26
        assert 2 <= max(row_len, column_len) <= 26, 'board legnth more, than 26'
        
        self.row_len = row_len
        self.column_len = column_len
        self.row_letters = row_letters.split('-')
        self.column_letters = column_letters.split('-')

class Board:
    """"
    Creates an instance of board with chess pieces in initial, positions using instance of BoardConfig class
    """
    def __init__(self, BoardConfig_instance, init_positions):
        self.BoardConfig_instance = BoardConfig_instance
        self.grid = dict()
        self.init_positions = dict()
        
        """Reads config file to find out inital positions and which squares contains which pieces"""
        # не передаю имя файла, зачем то передал сам файл!
        with shelve.open(init_positions, 'r') as db:
            for key, value in db.items():
                self.init_positions[key] = value
        
        """Creates full chess board"""
        for row_index in self.BoardConfig_instance.row_letters:
            for column_index in self.BoardConfig_instance.column_letters:
                key = f"{row_index}-{column_index}"
                self.grid[key] = None

        """Reaplces the empty squares with pieces"""
        self.grid.update(self.init_positions)
    
    def __repr__(self) -> str:
        """
        !!! позже реализовать нормальный return без всего говна с форами, который будет выводить
        в правильно порядке за счет создания ключей форматированием f"x-y"
        выводить будет принтом по 1 штуке за раз!!! (наверн)
        мейби сделать генератором
        """
        rows = dict()
        
        #
        for column_index in self.BoardConfig_instance.column_letters:
            rows[column_index] = dict()
            
        #
        for square_coordinates, piece in self.grid.items():
            square_coordinates = square_coordinates.split('-')
            column_index = square_coordinates[1]
            row_index = square_coordinates[0]
            rows[column_index][row_index] = piece
        
        #
        boardstr = ''
        for row in self.BoardConfig_instance.column_letters[::-1]:
            for square in self.BoardConfig_instance.row_letters:
                boardstr += f"{rows[row][square] if rows[row][square] else '▫'}    "
            #
            boardstr += '\n\n'
        return boardstr
    
    @staticmethod
    def set_piece(file, row_index, column_index, value):
        key = f"{row_index}-{column_index}"
        file[key] = value


def initial_positions(BoardConfig_instance, file_name, *args: tuple[str | None, str | None, type]) -> str:
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
#    with shelve.open(f'{file_name}.txt', 'n') as file:
    with shelve.open(file_name, 'n') as file:
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


if __name__ == '__main__':
    print('unittest')

    class Pawn:
        def __repr__(self) -> str:
            return '♙'
    class Knight:
        def __repr__(self) -> str:
            return '♘'
    class Bishop:
        def __repr__(self) -> str:
            return '♗'
    class Rook:
        def __repr__(self) -> str:
            return '♖'
    class Queen:
        def __repr__(self) -> str:
            return '♕'
    class King:
        def __repr__(self) -> str:
            return '♔'
    
    config = BoardConfig()
    positions_coordinates = ((None, '7', Pawn), (None, '2', Pawn), # two lines of pawns
                             ('a', '8', Rook), ('a', '1', Rook), ('h', '8', Rook), ('h', '1', Rook),
                             ('b', '8', Knight), ('b', '1', Knight), ('g', '8', Knight), ('g', '1', Knight),
                             ('c', '8', Bishop), ('c', '1', Bishop), ('f', '8', Bishop), ('f', '1', Bishop),
                             ('d', '8', Queen), ('d', '1', Queen), ('e', '8', King), ('e', '1', King))
    positions = initial_positions(config, 'default_chess', *positions_coordinates)
    board = Board(config, 'default_chess')
    print(board)