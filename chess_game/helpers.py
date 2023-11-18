def transform_move(i, di, p_n):
    '''
    Allows a move to either be added or subtracted to coordinate i
    '''
    if p_n:
        return i + di
    else:
        return i - di

def simulate_move(piece, move):
    piece.coordinates += move

def rollback_move(piece, move):
    piece.coordinates -= move

