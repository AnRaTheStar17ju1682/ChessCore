import pytest


from chesscore_pisca.movement_superclass import MovementMode
from chesscore_pisca import chess_board
from test_chess_board import path, Cat


class ForwardMovement(MovementMode):
        def func(self, board, position):
            return self.move(board, position, column=True)


def minicharge(board, mode, laplace_demon, start_position):
    for possible_move in mode(board, start_position):
        if type(possible_move) == str:
            laplace_demon[mode].append(possible_move)
        else:
            laplace_demon[mode].extend(possible_move)


@pytest.fixture
def start_position():
    return 'd-4'


@pytest.fixture
def board(path):
    config = chess_board.BoardConfig(row_len=7, column_len=7)
    chess_board.initial_positions(config, path, ('d', '4', Cat))
    board = chess_board.Board(config, path)
    
    return board


class TestMovementMode:
    standart_offset = 1
    reverse_offset = -1
    test_move_argnames = ('row', 'column', 'expected', 'offset')
    test_move_argvalues = (
        (True, False, 'e-4', standart_offset),
        (False, True, 'd-5', standart_offset),
        (True, True, 'e-5', standart_offset),
        (True, False, 'c-4', reverse_offset),
        (False, True, 'd-3', reverse_offset),
        (True, True, 'c-3', reverse_offset),
    )
    @pytest.mark.parametrize(argnames=test_move_argnames, argvalues=test_move_argvalues)
    def test_move(self, start_position, board, *, row, column, expected, offset):
        vposition = ForwardMovement().move(board, start_position,
                        row=row, column=column, offset=offset
                    )
        
        assert vposition == expected
    
    
    def test_call(self, board, start_position):
        mode = ForwardMovement()
        laplace_demon = {mode: []}
        
        minicharge(board, mode, laplace_demon, start_position)
        
        expected_moves = sorted(laplace_demon[mode])
        assert expected_moves == ['d-5', 'd-6', 'd-7']
    
    
    def test_call_limited(self, board, start_position):
        mode = ForwardMovement(2)
        laplace_demon = {mode: []}
        
        minicharge(board, mode, laplace_demon, start_position)
        
        assert 'd-7' not in laplace_demon[mode]
    
    
    def test_call_way_blocked(self, board, start_position):
        mode = ForwardMovement()
        laplace_demon = {mode: []}
        
        board.grid['d-6']['piece'] = Cat()
        
        minicharge(board, mode, laplace_demon, start_position)
        
        assert 'd-7' not in laplace_demon[mode]