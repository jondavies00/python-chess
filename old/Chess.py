from termcolor import colored, cprint
import numpy as np

class Board():
    def __init__(self):
        # The board is a numpy array. The board automatically 'flips' vertically after each turn, therfore meaning the files (a-h) stay the same, but the ranks stay the same.
        # This means movesets can be defined as the same for both black and white pieces, as the colour is checked, and THEN whether the move is in the moveset.
        # You still need to reference the correct squares though. 'e2' for white is the king pawn, but 'e2' for black is not the black's king's pawn. This would be 'e7'
        self.board = np.array([
            [Rook('white'), Knight('white'), Bishop('white'), Queen('white'),King('white'), Bishop('white'), Knight('white'), Rook('white')],

            [Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'),Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')],

            [None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None],

            [Pawn('grey'), Pawn('grey'), Pawn('grey'), Pawn('grey'),Pawn('grey'), Pawn('grey'), Pawn('grey'), Pawn('grey')],

            [Rook('grey'), Knight('grey'), Bishop('grey'), Queen('grey'),King('grey'), Bishop('grey'), Knight('grey'), Rook('grey')]
        ])
    
    def move(self, piece_symbol, old_loc,new_loc, player):
        #TODO: check move is in moveset
        new_rank, new_file = new_loc[0], new_loc[1]
        old_rank, old_file = old_loc[0], old_loc[1]
        # To traverse the board, we go ranks first, then files. The first board coordinate is 0,0 
        # want a positive rank, so use old - new (i.e. old pawn rank could be 6 (2) and new would be 4 (4), giving a move of +2)
        piece_to_move = self.get_piece(old_loc)
        if self.found_piece(piece_symbol, player.colour, piece_to_move):
            
            if self.legal_move(piece_to_move, old_loc, new_loc, player):
                self.board[old_rank][old_file] = None
                self.board[new_rank][new_file] = piece_to_move
                return True
            else:
                return False
        else:
            return False

    def legal_move(self, piece=object, old_loc=tuple, new_loc=tuple, player=object):
        new_rank, new_file  = new_loc[0], new_loc[1]
        old_rank, old_file = old_loc[0], old_loc[1]
        move = (old_rank - new_rank, new_file - old_file)
        if move in piece.moveset or move in piece.capture_set:
            #TODO: Is move check? Is the move illegal (i.e. reveals king)
            # perform simulated move, 
            if reveal_king(move, player.colour):
                return False
            

            #great, now make sure no piece is blocking the move.
            # 1. Can piece reach target square?

            if move[0] == 0: # horizontal move
                if move[1] > 0:
                    step_file = 1
                else:
                    step_file = -1
                check_file = old_file + step_file
                while check_file != new_file:
                    
                    if self.board[old_rank][check_file] != None:
                        return False
                    check_file += step_file
            
            if move[1] == 0: # vertical move
                if move[0] > 0:
                    step_rank = -1
                else:
                    step_rank = 1
                check_rank = old_rank + step_rank #start checking next rank (current square is occupied by itself)
                while check_rank != new_rank:

                    if self.board[check_rank][old_file] != None:
                        return False      
                    check_rank += step_rank
            elif abs(move[0]) == abs(move[1]): # diagonal move

                if move[1] > 0: #IF MOVE IS POSITIVE IN THE FILE DIRECTION
                    step_file = 1
                else:
                    step_file = -1
                if move[0] > 0: #IF MOVE IS POSITIVE IN THE RANK DIRECTION
                    step_rank = -1
                else:
                    step_rank = 1 
                check_pos = old_loc
                check_pos = check_pos[0] + step_rank, check_pos[1] + step_file
                new_pos = new_loc
                while check_pos != new_pos:
                    
                    if self.board[check_pos[0]][check_pos[1]] != None:
                        return False
                    check_pos = check_pos[0] + step_rank, check_pos[1] + step_file


            # 2. Is same colour piece blocking the target square? If so, can't move, if enemy (and the move is in the capture moveset), capture.
            if self.board[new_rank][new_file] != None: #something in target square
                target_piece = self.board[new_rank][new_file]
                if target_piece.colour != player.colour and move in piece.capture_set: #capture
                    print(player.colour, "captured", target_piece.colour, target_piece, ".")
                    player.update_points(target_piece.value)
                    print(player.colour, "now has", player.points, "points.")
                    return True
                elif target_piece.colour == player.colour:
                    print("Can't move to square: same colour blocking")
                    return False
            else:
                return True
        else:
            return False

    
    def get_piece(self, location):
        return self.board[location[0]][location[1]]

    def found_piece(self, symbol, colour, piece):
        if piece == None:
            return False
        elif piece.symbol == symbol and piece.colour == colour:
            return True 
        else:
            return False


    def flip(self):
        self.board = np.flip(self.board, axis=0)

    def __repr__(self):
        board_string = ''
        files = 8 # x
        rows = 8 # y
        for f in range(files):
            board_string += '| '
            for r in range(rows):
                piece = self.board[f][r]

                piece_symbol = repr(piece)

                if piece == None:
                    board_string += colored(' ')

                elif piece.colour == 'white':
                    board_string += piece_symbol
                else:
                    board_string += piece_symbol
                board_string += ' | '

                # board_string += self.board[f][r]
            board_string += '\n'
        return board_string

# Define pieces
# note: movesets are defined as (y,x) tuples, not (x,y). This is because the board is defined as moving down ranks as moving down 'y', and files as 'x'

class Pawn():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "p"
        self.value = 1

        self.moveset = [(1,0),(2,0)] 
        self.capture_set = [(1,1),(1,-1)]


    def __repr__(self):

        return colored(self.symbol, self.colour)

class Rook():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "R"
        self.moveset = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                        (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),
                        (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __repr__(self):
        return colored(self.symbol, self.colour)
        
class Knight():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "N"
        self.moveset = [(1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1)]
        self.capture_set = self.moveset
        self.value = 3

    def __repr__(self):
        return colored(self.symbol, self.colour)

class Bishop():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "B"
        self.moveset = [
                        (0, 0), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __repr__(self):
        return colored(self.symbol, self.colour)

class King():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "K"
        self.moveset = [(0,1), (1,1), (1,0), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        self.capture_set = self.moveset
        self.value = 1000
    def __repr__(self):
        return colored(self.symbol, self.colour)
    
class Queen():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "Q"
        self.moveset = [(0, 0), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
                        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0,-1), (0,-2), 
                        (0,-3), (0,-4), (0,-5), (0,-6), (0,-7), (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 10
    def __repr__(self):
        return colored(self.symbol, self.colour)

class Player():

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.points = 0

    def update_points(self, piece_value):
        self.points += piece_value

class Game():

    piece_symbols = ['p','B','R','N','K','Q']

    notation_to_coordinate = {
        'a':7,
        'b':6,
        'c':5,
        'd':4,
        'e':3,
        'f':2,
        'g':1,
        'h':0
    }


    def start(self):
        player1 = Player('p1', 'white')
        player2 = Player('p2', 'grey')

        game_board = Board()
        game_ended = False
        to_play = player1
        while not game_ended:
            game_board.flip()
            print(game_board)
            if to_play.colour == 'white':
                print('White to move... ')
            elif to_play.colour == 'grey':
                print('Black to move... ')

            valid = False

            while not valid:
                move_input = input("ENTER MOVE (notation: (piece symbol) (location) (new_location), use 'p' for pawn): ")
                
                if not self.valid_input(move_input):
                    valid = False
                    print("Invalid input, try again")
                else:
                    piece, old_loc, new_loc = self.decode_move(move_input, to_play.colour) #e.g. a2 a3 to move pawn to a3
                    

                    if game_board.move(piece, old_loc, new_loc, to_play):
                        valid = True
                        print(piece, old_loc, new_loc)
                    else:
                        valid = False
                        print("Invalid move, try again.")
                    
            if to_play.points >= 1000: #king captured
                print(to_play.colour, "wins!")
                break

            if to_play.colour == 'white':
                to_play = player2
            elif to_play.colour == 'grey':
                to_play = player1
        
    def valid_input(self, move_input):
        try:
            a, b, c = move_input.split(' ')
        except:
            return False
        if len(a) != 1:
            return False
        elif len(b) != 2:
            return False
        elif len(c) != 2:
            return False
        elif a not in Game.piece_symbols or b[0] not in Game.notation_to_coordinate or c[0] not in Game.notation_to_coordinate:
            return False
        elif int(b[1]) > 8 or int(b[1]) < 1 or int(c[1]) > 8 or int(c[1]) < 1:
            return False
        else:
            return True
    
    def decode_move(self, move, colour):
        #moves will be a simplified notation where player inputs 'movefrom' square and 'moveto'
        piece_symbol, move_from, move_to = move.split(' ')

        old_loc = 0,0
        new_loc = 0,0
        if colour == 'white':
            modifier1 = 8
            modifier2 = -1
        else:
            modifier1 = -1
            modifier2 = 1
        
        #piece_name = Game.symbol_to_piece_name[piece_symbol]
        old_loc =  modifier2 * int(move_from[1]) +modifier1, 7-Game.notation_to_coordinate[move_from[0]] #e.g. a4 gets converted to 0, 3
        new_loc = modifier2 * int(move_to[1]) + modifier1, 7-Game.notation_to_coordinate[move_to[0]]
        return piece_symbol, old_loc, new_loc

game = Game()
game.start()

