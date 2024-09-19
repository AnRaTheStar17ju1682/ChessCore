import pytest
import unittest.mock as umock
import shelve


from chesscore_pisca import chess_board # type: ignore


def Cat():
    cat = umock.MagicMock()
    cat.charge.return_value = None
    cat.decrease_remaining_usages.return_value = None
    cat.__str__.return_value = "k"
    possible_moves = tuple(f"{row_index}-{column_index}"
                           for row_index in 'abc'
                           for column_index in '12')
    cat.laplace_demon = {'mode': possible_moves}
    cat.remaining_modes_usages = {
        float('inf'): ['mode'],
        0: []
    }
    return cat


@pytest.fixture
def mock_config(mocker):
    conf = mocker.Mock()
    
    conf.row_len = 3
    conf.column_len = 3
    conf.row_letters = 'a-b-c'.split('-')
    conf.column_letters = '1-2-3'.split('-')
    
    return conf


@pytest.fixture
def path(tmp_path):
    return (str(tmp_path) + '/test_setup')

class TestBoardConfig:
    def test_board_config_default_values(self):
        config = chess_board.BoardConfig()
        
        assert config.row_len == 8
        assert config.column_len == 8
        assert config.row_letters == 'a-b-c-d-e-f-g-h'.split('-')
        assert config.column_letters == '1-2-3-4-5-6-7-8'.split('-')
    
    
    def test_board_config_with_words_as_indeces(self):
        config = chess_board.BoardConfig(row_len=2, row_letters='hor1-hor2')
        
        assert config.row_letters == 'hor1-hor2'.split('-')
    
    
    def test_board_config_different_sides_length(self):
        config = chess_board.BoardConfig(row_len=3, column_len=7)
    
    
    def test_board_config_longer_than_default(self):
        config = chess_board.BoardConfig(
            row_len=10, column_len=10,
            row_letters='a-b-c-d-e-f-g-h-x-y', 
            column_letters='1-2-3-4-5-6-7-8-9-10'
        )
    
    
    def test_board_config_fail_cause_short(self):
        with pytest.raises(AssertionError, match='both lenghts lesser, than 2'):
            config = chess_board.BoardConfig(row_len=1, column_len=1)
    
        
    def test_board_config_fail_cause_too_long(self):
        with pytest.raises(AssertionError, match='the lenght of some side more, than 26'):
            config = chess_board.BoardConfig(
                row_len=27,
                row_letters='a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z-a1'
            )
        
        with pytest.raises(AssertionError, match='the lenght of some side more, than 26'):
            config = chess_board.BoardConfig(
                column_len=27,
                column_letters='1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18 \
                -19-20-21-22-23-24-25-26-27'
            )


class TestInitialPositions():
    def test_inital_positions(self, mock_config, path):
        positions = (('a', '1', 'cat'), ('a', '2', 'dog'))
        
        chess_board.initial_positions(
            mock_config,
            path,
            *positions
        )
        
        with shelve.open(path, 'r') as db:
            assert db['a-1'] == 'cat'
            assert db['a-2'] == 'dog'
    
    
    @pytest.mark.parametrize(
        argnames='square',
        argvalues=(('d', '1', 'cat'), ('a', '4', 'cat'))
    )
    def test_out_of_the_boardconfig_range(self, mock_config, path, square):
        extra_letter = 'd' if square[0]=='d' else '4'
        boundary = 'row' if square[0]=='d' else 'column'
        
        error_message =  f'{extra_letter} is not in the board_config {boundary}_letters'
        
        with pytest.raises(AssertionError, match=error_message):
            chess_board.initial_positions(
                mock_config,
                path,
                square
            )
    
    
    def test_one_coordinate_given(self, mock_config, path):
        positions = ((None, '3', 'cat'), ('a', None, 'cat'))
        
        chess_board.initial_positions(mock_config, path, *positions)
        
        with shelve.open(path, 'r') as db:
            assert db['a-3'] == 'cat'
            assert db['b-3'] == 'cat'
            assert db['c-3'] == 'cat'
            assert db['a-1'] == 'cat'
            assert db['a-2'] == 'cat'
    
    
    def test_overlapping(self, mock_config, path):
        positions = ((None, '3', 'cat'), ('a', None, 'dog'))
        
        chess_board.initial_positions(mock_config, path, *positions)
        
        with shelve.open(path, 'r') as db:
            assert db['a-3'] == 'dog'
            assert db['b-3'] == 'cat'
            assert db['c-3'] == 'cat'
            assert db['a-1'] == 'dog'
            assert db['a-2'] == 'dog'
    
    
    def test_piece_not_given(self, mock_config, path):
        error_message = 'func recieved arg without a piece class'
        with pytest.raises(AssertionError, match=error_message):
            chess_board.initial_positions(mock_config, path, ('a', '1', None))

class TestBoard:
    @pytest.fixture
    def init_positions_config(self, mock_config, path):
        positions = ((None, '1', Cat), (None, '3', Cat))
        
        chess_board.initial_positions(mock_config, path, *positions)

        return path
    
    
    @pytest.fixture
    def board(self, mock_config, init_positions_config):
        return chess_board.Board(mock_config, init_positions_config)
        
    
    def test_board_init(self, board):
        assert board
    
    
    def test_board_move(self, board):
        board.move_piece('a-1', 'b-2')
        
        assert board.grid['a-1']['piece'] == None
        assert board.grid['b-2']['piece'] != None
        
        board.grid['b-2']['piece'].decrease_remaining_usages.assert_called_with('mode')
    
    
    def test_board_move_on_unpossible(self, board):
        with pytest.raises(AssertionError, match="this piece can't make such a move"):
            board.move_piece('a-1', 'b-3')
    
    
    def test_try_to_move_blank_square(self, board):
        with pytest.raises(AssertionError, match='there no piece in this square'):
            board.move_piece('a-2', 'b-2')
    
    
    def test_try_to_move_on_unexisting_square(self, board):
        with pytest.raises(AssertionError, match="the try to move on a unexisting square"):
            board.move_piece('a-1', 'b-4')
    
    
    def test_try_to_move_unexisting_square(self, board):
        with pytest.raises(AssertionError, match="the try to move a unexisting square"):
            board.move_piece('a-4', 'b-2')
    
    
    def test_board_str_function(self, board):
        assert str(board) == 'k    k    k    \n\n▫    ▪    ▫    \n\nk    k    k'