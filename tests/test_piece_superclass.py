import pytest
import unittest.mock as mock


from chesscore_pisca import piece_superclass

@pytest.fixture
def piece():
    class DumbPiece(piece_superclass.Piece):
        ico = '@'
        starting_remaining_modes_usages = {
            float('inf'): ['spam'],
            2: ['eggs'],
            1: ['ni']
        }
    
    return DumbPiece()
class TestPiece:
    def test_init_dictionary_equality(self, piece):
        # by default starting_remaining_modes_usages donesn't have a "0" key,
        # so i'll add it for a test
        piece.starting_remaining_modes_usages[0] = []
        assert piece.remaining_modes_usages == piece.starting_remaining_modes_usages
    
    
    # a instance single-use dictionary MUST DO NOT impact on a class dictionary
    def test_init_dictionary_discreteness(self, piece):
        assert piece.remaining_modes_usages is not piece.starting_remaining_modes_usages
    
    
    def test_init_dictionary_discreteness(self, piece):
        for key in piece.starting_remaining_modes_usages:
            # lists must be different
            assert piece.remaining_modes_usages[key] is not piece.starting_remaining_modes_usages[key]
            # modes must be the same
            assert piece.remaining_modes_usages[key][0] is piece.starting_remaining_modes_usages[key][0]
    
    
    def test_str(self, piece):
        assert str(piece) == '@'
    
    
    def test_decrease_remaining_usages(self, piece):
        piece.decrease_remaining_usages('ni')
        assert 'ni' in piece.remaining_modes_usages[0]
    
    
    def test_charge(self, mocker):
        moves_list = (
            'a-1', 'a-2',
            ('b-3'),
            ('c-4', 'c-5')
        )
        mode_mock = mocker.Mock(return_value=moves_list)
        
        class JustPiece(piece_superclass.Piece):
            ico = '@'
            starting_remaining_modes_usages = {1: [mode_mock]}
            
        piece = JustPiece()
        
        # piece.cahrge(board=mocker.mock(), position=mocker.mock())
        piece.charge(mocker.Mock(), mocker.Mock())
        
        assert piece.laplace_demon[mode_mock] == ['a-1', 'a-2', 'b-3', 'c-4', 'c-5']