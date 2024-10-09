from copy import deepcopy


def display_moves(board, main_square, contrast=False):
    board = deepcopy(board)
    main_piece = board.grid[main_square]['piece']
    for square in board.grid:
        for mode in main_piece.laplace_demon:
            if square in main_piece.laplace_demon[mode]:
                piece = board.grid[square]['piece']
                color = board.grid[square]['color']
                if contrast:
                    board.grid[square]['piece'] = "\033[31m●\033[0m"
                else: 
                    if piece:
                        board.grid[square]['piece'] = f"\033[1;32m{piece}\033[0m" 
                    else:
                        color = '▫' if color == 'w' else '▪'
                        board.grid[square]['piece'] = f"\033[1;32m{color}\033[0m"
    piece_char = str(board.grid[main_square]['piece'])
    board.grid[main_square]['piece'] = f'\033[1;31m{piece_char}\033[0m'
    print(str(board), '_'*42, sep='\n')


def display_moves_extended(board, main_square, contrast=False):
    print('lapalce:', board.grid[main_square]['piece'].laplace_demon, '\n',
                  'remaining modes:', board.grid[main_square]['piece'].remaining_modes_usages)
    display_moves(board, main_square, contrast)


def fast_display_piece_moves(piece_class, *, then_move = None, extended = False):
    from chesscore_pisca import chess_board
    
    
    if extended:
        display = display_moves_extended
    else:
        display = display_moves
    
    
    position = 'e-5'
    config = chess_board.BoardConfig(row_len=9, column_len=9)
    
    board = chess_board.Board(config)
    board.grid[position]['piece'] = piece_class()
    board.grid[position]['piece'].charge(board, position)
    
    display(board, position)
    
    
    if then_move is not None:
        if type(then_move) is str:
            then_move = (then_move,)
        current_position = position
        for new_position in then_move:
            board.move_piece(current_position, new_position)
            display(board, new_position)
            current_position = new_position