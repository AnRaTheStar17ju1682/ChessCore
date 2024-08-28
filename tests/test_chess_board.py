import pytest


from chesscore_pisca import chess_board # type: ignore


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
        with pytest.raises(raises=AssertionError, match='both lengths lesser, than 2'):
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