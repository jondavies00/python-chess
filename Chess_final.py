from termcolor import colored
import random 
import colorama
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


    

# Made up of pieces (pawns, rooks etc)
# functions to get piece at coordinate
# functions to change coordinates of pieces
class Board:
    '''
    Board is set up as a list of pieces. There are ranks and files too. Board can be printed, and flipped so whoever is playing
    can have a better view of the board.
    '''
    ranks = [1,2,3,4,5,6,7,8]
    files = ['a','b','c','d','e','f','g','h']

    def __init__(self):
        self.pieces = [Rook('white', (0,0)), Knight('white', (1,0)), Bishop('white',(2,0)), Queen('white',(3,0)), King('white', (4,0)), Bishop('white', (5,0)), Knight('white',(6,0)), Rook('white',(7,0)),
                        Pawn('white', (0,1)), Pawn('white', (1,1)), Pawn('white',(2,1)), Pawn('white',(3,1)),Pawn('white', (4,1)), Pawn('white', (5,1)), Pawn('white',(6,1)), Pawn('white',(7,1)),
                        Rook('black', (0,7)), Knight('black', (1,7)), Bishop('black',(2,7)), Queen('black',(3,7)), King('black', (4,7)), Bishop('black', (5,7)), Knight('black',(6,7)), Rook('black',(7,7)),
                        Pawn('black', (0,6)), Pawn('black', (1,6)), Pawn('black',(2,6)), Pawn('black',(3,6)),Pawn('black', (4,6)), Pawn('black', (5,6)), Pawn('black',(6,6)), Pawn('black',(7,6))]
    
    def move_piece(self, p, new_coords):
        '''Moves a piece to 'new_coords' by updating the piece's coordinates.'''
        p.coordinates = new_coords

    def capture_piece(self, p, new_coords):
        '''Finds target piece, and returns its value.'''
        for piece in self.pieces:
            if piece.coordinates == new_coords:
                captured = piece
                self.piece.remove(piece)
        return captured.value

    def piece_in_square(self, coords):
        '''Return whether a piece exists at the given coordinate'''
        for p in self.pieces:
            if p.coordinates == coords:
                return True
        return False

    def get_piece(self, coords):
        '''Returns the piece at given coordinates.'''
        for p in self.pieces:
            if p.coordinates == coords:
                return p
        return None

    def find_piece(self, piece_symbol, piece_colour):
        '''Find and return a piece, given its symbol and colour.'''
        for piece in self.pieces:
            if piece.symbol == piece_symbol and piece.colour == piece_colour:
                return piece

    def remove_piece(self, piece):
        '''Remove a piece from the board'''
        self.pieces.remove(piece)

    def add_piece(self, piece):
        self.pieces.append(piece)

    def is_blocked(self, old_square, new_square):
        '''
        Takes the squares a piece wants to move from, and to, as well as its move and checks the squares between them.
        If any square has a piece in it then return true, otherwise false.
        Since blockable moves can only be diagonal, horizontal, or vertical, we only need to check these cases.
        
        Keyword arguments:\n
        old_square -- the square the piece is moving from\n
        new_square -- the square the piece is moving to

        Returns:\n
        A boolean value based on whether the path is blocked.
        '''
        move = new_square[0] - old_square[0], new_square[1] - old_square[1]

        #If the move is a negative vector, we want to step down, and step up otherwise
        if move[0] > 0:
            step_x = 1
        else:
            step_x = -1
        if move[1] > 0:
            step_y = 1
        else:
            step_y = -1

        # Start from the old square
        x = old_square[0]
        y = old_square[1]

        if move[1] == 0:  # Horizontal move
            while x != new_square[0]-step_x: # While the current x we are incrementing has not reached the square before the desired one
                x += step_x
                if self.piece_in_square((x,y)):
                    return True
        elif move[0] == 0: # Vertical move
            while y != new_square[1]-step_y:
                y += step_y
                if self.piece_in_square((x,y)):
                    return True
        elif abs(move[0]) == abs(move[1]): # Must be a diagonal move
            while x != new_square[0]-step_x and y != new_square[1]-step_y:
                x, y = x + step_x, y + step_y
                if self.piece_in_square((x,y)):
                    return True
        else:
            # If none of the others, the move must either be a single square, or a knight move. Either way we check if anything 
            # is on that square in the 'valid move' section of the code.
            return False  

    def flip(self):
        self.ranks.reverse()

    def __str__(self):
        gb_string = ''
        color = ''
        back_colour = ''
        
        even_rank = True
        even_file = True
        found_piece = None
        for r in self.ranks:
            gb_string += str(r) + ''
            for f in range(0, len(self.files)):
                if even_rank:

                    if even_file == 0:
                        back_color = 'on_grey' #switch to on_white
                    else:
                        back_color = 'on_grey'
                else:
                    if even_file == 0:
                        back_color = 'on_grey'
                    else:
                        back_color = 'on_grey'#switch to on_white

                for p in self.pieces:
                    if (p.coordinates) == (f,r-1):
                        if p.colour == 'black':
                            color = 'blue'
                        else:
                            color = 'white'
                        found_piece = p
                        break
                        
                if found_piece != None :
                    gb_string += '|' +colored(str(p), color, back_color) + ''
                else: 
                    if back_color == 'on_white': #switch to on_white
                        color = 'grey'
                    else:
                        color = 'white'
                    gb_string+= colored('| ', color, back_color)
                found_piece = None

                even_file = not even_file
            even_rank = not even_rank

            gb_string+='|\n'
        gb_string += '  a b c d e f g h'
        return gb_string


# Pieces have coordinates, colour, movesets, and capture sets
# Only pawns have movesets != capture sets

class Pawn:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "p"
        self.value = 1

        self.moveset = [(0,1),(0,2)] 
        self.capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)]


    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

class Rook:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "R"
        self.moveset = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                        (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),
                        (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

class Knight:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "N"
        self.moveset = [(1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1)]
        self.capture_set = self.moveset
        self.value = 3

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

class Bishop:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "B"
        self.moveset = [
                        (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

class King:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "K"
        self.moveset = [(0,1), (1,1), (1,0), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        self.capture_set = self.moveset
        self.value = 1000
    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'
    
class Queen:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "Q"
        self.moveset = [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
                        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0,-1), (0,-2), 
                        (0,-3), (0,-4), (0,-5), (0,-6), (0,-7), (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 10
    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'


# Player has colour, name, and possible moves they can choose
class Player():

    def __init__(self, name, colour, human):
        self.name = name
        self.colour = colour
        self.points = 0
        self.human = human
        #self.in_check = False
        self.possible_squares = {}
        #self.capture_squares = {}


    def update_points(self, piece_value):
        self.points += piece_value

    def update_possible_squares(self, board, opponent, check_for_check):
        '''
        Updates the 'possible squares' dictionary for the player. The dictionary maps player's pieces to squares that
        those pieces can move to.

        param board: the game board
        param opponent: the player's opponent
        '''
        
        ####
        # UPDATING POSSIBLE SQUARES
        # Loop through every piece of colour
        # Generate all the squares that the piece could reach given its moveset
        # This means no negative squares, and no squares with pieces already on them
        
        # Can check if piece can reach square too
        ####
        self.possible_squares = {}
        my_pieces = [mp for mp in board.pieces if mp.colour == self.colour]

        ## Black pawns will be moving up (oldsq needs to subtract the move if moving from black side)
        if self.colour == 'white':
            modifier = True #positive
        else:
            modifier = False #negative

        for piece in my_pieces:
            self.possible_squares[piece] = []
            #self.capture_squares[piece] = []

        # TODO: If we are in check, we cannot have possible moves/captures that do not get us out of check. 
        #       Need a function 'simulate move' that does the generated move for each piece (if in check). If the move results in a position
        #       no longer in check, add it to the possible moves and 'rollback' the move.
        #       Checkmate happens when we are in check, and NO possible moves or captures are available.
        #       We should check the list in the 'Game' class.

        # Go through each piece of same colour, and go through all the moves in its moveset. Then, add it to either capture moves or possible moves
        # respectively.

        for piece in my_pieces:
            poss_moves = []
            poss_captures = []



            if piece.symbol == 'B':
                pass
            
            for m in list(set(piece.moveset + piece.capture_set)): # add two lists together, remove dupesa2 
                
                new_x = transform_move(piece.coordinates[0], m[0], modifier)
                new_y = transform_move(piece.coordinates[1], m[1], modifier)
                desired_square = (new_x, new_y)

                if piece.symbol == 'K' and desired_square in opponent.possible_squares:
                    pass
                elif new_x > 7 or new_x < 0 or new_y > 7 or new_y < 0:
                    pass
                elif board.is_blocked(piece.coordinates, desired_square):
                    pass
                elif board.piece_in_square(desired_square) and board.get_piece(desired_square).colour == self.colour:
                    pass
                #capturing with a white pawn -> must be a forward capture
                #if its a back capture, we cant allow
                elif piece.symbol == 'p' and m[1] < 0: 
                    pass
                elif piece.symbol == 'p' and m[1] < 0:
                    pass
                # If there is an *enemy* *piece* in the desired square and it's a *capture move*
                elif board.piece_in_square(desired_square) and board.get_piece(desired_square).colour != self.colour and m in piece.capture_set:

                    if self.in_check(board, opponent):
                        print(self.name, "is in check.")
                        if self.move_gets_self_out_of_check(board, piece, desired_square, opponent):
                            print("A move gets me out of check: ", str(piece), str(piece.coordinates), str(desired_square))
                            poss_moves.append(desired_square)
                        else:
                            pass

                    elif check_for_check:
                        if not self.move_results_in_self_check(board, piece, desired_square, opponent):
                            poss_moves.append(desired_square)
                        else:
                            print(self.colour, "looked at", piece.colour)
                            print("A move would result in self check: ", str(piece), str(piece.coordinates), str(desired_square))
                            pass
                    else:
                        poss_moves.append(desired_square)
                # If there is no piece in the desired square, and it's not a capture move
                elif not board.piece_in_square(desired_square) and m in piece.moveset:
                    if self.in_check(board, opponent):
                        print(self.name, "is in check.")
                        if self.move_gets_self_out_of_check(board, piece, desired_square, opponent):
                            print("A move gets me out of check: ", str(piece), str(piece.coordinates), str(desired_square))
                            poss_moves.append(desired_square)
                        else:
                            pass
                    elif check_for_check:
                        if not self.move_results_in_self_check(board, piece, desired_square, opponent):
                            poss_moves.append(desired_square)
                        else:
                            print(self.colour, "looked at", piece.colour)
                            print("A move would result in self check: ", str(piece), str(piece.coordinates), str(desired_square))
                    else:
                        poss_moves.append(desired_square)
                else:
                    pass

            self.possible_squares[piece] = poss_moves
            #self.capture_squares[piece] = poss_captures

    def move_results_in_self_check(self, board, piece, desired_square, opponent):
        opponent_current_squares = opponent.possible_squares

        #save prior coords
        before_coords = piece.coordinates
        #if a piece gets captured, we need to save it
        captured = board.get_piece(desired_square)
        #temporarily remove the piece

        if captured != None:
            if captured.symbol == 'K':
                return False
            else:
                board.remove_piece(captured)

        #perform move
        piece.coordinates = desired_square
        #update opponent's possible move squares now we simulated the move
        opponent.update_possible_squares(board, self, False)
        in_check = self.in_check(board, opponent)
        piece.coordinates = before_coords
        if captured != None:
            board.add_piece(captured)
        #opponent.update_possible_squares(board, self, False)
        opponent.possible_squares = opponent_current_squares
        return in_check
        
    def move_gets_self_out_of_check(self, board, piece, desired_square, opponent):
        #save prior coords
        opponent_current_squares = opponent.possible_squares
        
        #save move squares
        before_coords = piece.coordinates

        #if a piece gets captured, we need to save it
        captured = board.get_piece(desired_square)
        #temporarily remove the piece, if its the king we know its a check
        if captured != None:
            if captured.symbol == 'K':
                return False
            else:
                board.remove_piece(captured)
        #perform move
        piece.coordinates = desired_square

        #update opponent's possible move squares now we simulated the move
        opponent.update_possible_squares(board, self, False)
        #see if we are no longer in check
        no_longer_in_check = not self.in_check(board, opponent)
        #rollback changes
        piece.coordinates = before_coords
        if captured != None:
            board.add_piece(captured)
        
        #opponent.update_possible_squares(board, self, False)
        opponent.possible_squares = opponent_current_squares
        return no_longer_in_check


    def in_check(self, board, opponent):
        '''
        Goes through the opponent's possible squares. If my king is in them, set 'check' to true
        '''

        check = False
        king_pos = board.find_piece('K', self.colour).coordinates
        opponent_attacking_squares = opponent.possible_squares
        #print("Opponents possible moves: ", opponent_attacking_squares)
        #print("My king position: ", king_pos)
        for piece in opponent_attacking_squares:

            if king_pos in opponent_attacking_squares[piece]:
                #print("check")
                check = True
                
        return check

    def in_checkmate(self, board, opponent):
        #If there are no possible moves, it is checkmate.
        checkmate = True
        for piece in self.possible_squares:
            if len(self.possible_squares[piece]) > 0:
                checkmate = False
        return checkmate

    def __str__(self):
        return self.name

# Game has the board, and the players
class Game:

    def __init__(self, white_name, black_name):
        # Inititialise game settings
        # room for additional parameters such as turn time etc
        self.game_board = Board()
        self.player_1 = Player(white_name, 'white', True)
        self.player_2 = Player(black_name, 'black', False)

        self.winner = None
        self.loser = None
        self.win_type = None
        self.draw = False
        self.finished = False
        self.move_history = []

    def game_loop(self):
        p1 = self.player_1
        p2 = self.player_2
        board = self.game_board
        to_play = p1
        opponent = p2
        while not self.finished:
            board.flip()
            print(str(to_play) + " it is your go.")
            print(board)
            
            moved = False

            #UPDATE VALID MOVES 
            self.update_player_moves(board, to_play, opponent)
            if to_play.in_checkmate(board, opponent):
                finished = True
                self.winner = opponent
                self.loser = to_play
                self.win_type = 'checkmate'
                break

            poss_moves = to_play.possible_squares
            #print(str(to_play),"'s possible moves: ", poss_moves)

            #Get player input
            while not moved:
                try:
                    if to_play.human:
                        sq1, sq2 = input('Enter squares: ').split(' ')

                        coord1 = self.square_to_coord(sq1)
                        coord2 = self.square_to_coord(sq2)
                    else:
                        coord1, coord2 = self.pick_random_move(poss_moves)
                        print("%s (AI) picked %s to %s." % (to_play.name, self.coord_to_square(coord1), self.coord_to_square(coord2)))

                    self.move(coord1, coord2, board, to_play)

                    print("Moved. %s points = %i" % (str(to_play), to_play.points))
                    moved = True
                except Exception as e: 
                    print("Invalid move, try again.")
                    print("Error was: " + str(e))
                    moved = False

            print(self.move_history)
            #UPDATE VALID MOVES AGAIN
            self.update_player_moves(board, to_play, opponent)
            if to_play == p1:
                to_play = p2
                opponent = p1
            else:
                to_play = p1 
                opponent = p2
        
        print(self.get_aftermatch_stats())
    
    def move(self, from_, to_, board, player):
        # get the piece we want to move
        piece_to_move = board.get_piece(from_)

        if piece_to_move.colour != player.colour:
            raise ValueError("Opponent's piece was selected.")
        elif piece_to_move == None:
            raise ValueError("No piece at desired *from* square.")
        elif to_ not in player.possible_squares[piece_to_move]:
            raise ValueError("Move is not a valid move. Either path is blocked, same coloured piece exists at target square, or move results in self-check")
        else:

            #from here, we assume the move is valid
            #if there is a piece where we are moving to, it has to be captured (as its a valid move)
            capture_piece = board.get_piece(to_)
            if capture_piece != None:
                board.remove_piece(capture_piece)
                player.update_points(capture_piece.value)
            # move it to the desired position
            self.game_board.move_piece(piece_to_move, to_)
            self.move_history.append(str(piece_to_move) + str(self.coord_to_square(to_)))
            if piece_to_move.symbol == 'p' and (to_[1] == 7 or to_[1] == 0):
                self.promote_pawn(piece_to_move, board)

    def promote_pawn(self, pawn, board):
        promoted = Queen(pawn.colour, pawn.coordinates)
        board.remove_piece(pawn)
        board.add_piece(promoted)



    def update_player_moves(self, board, player, opponent):
        player.update_possible_squares(board, opponent, True)

    def get_aftermatch_stats(self):
        winner_points = self.winner.points
        loser_points = self.loser.points
        winner_name = self.winner.name
        loser_name = self.loser.name
        if self.win_type == 'checkmate':

            stat_string = ("%s won by checkmating %s" % (winner_name, loser_name))
        elif self.win_type == 'time':
            stat_string = ("%s won on time." % winner_name)
        elif self.win_type == 'draw':
            stat_string = ("Nobody won. Draw.")
        
        stat_string += '\n%s points: %i\n%s points: %i\nThanks for playing!' % (winner_name, winner_points, loser_name, loser_points)
        return stat_string
    
    def square_to_coord(self, sq):
        try:
            file_ = sq[0]
            rank_ = int(sq[1])
            file_ = Board.files.index(file_)
            return file_, rank_-1
        except:
            raise ValueError("Invalid input.")
    
    def coord_to_square(self, coord):
        try:
            file_ = coord[0]
            rank_ = coord[1]
            file_ = Board.files[file_]
            
            return file_ + str(rank_+1)
        
        except:
            raise ValueError("Invalid input.")
        
    def is_blocked(self, move, old_square, new_square):

        #If the move is a negative vector, we want to step down, and step up otherwise
        if move[0] > 0:
            step_x = 1
        else:
            step_x = -1
        if move[1] > 0:
            step_y = 1
        else:
            step_y = -1
        #ignore current square and new square
        x = old_square[0]
        y = old_square[1]
        if move[1] == 0: #horizontal move
            while x != new_square[0]-step_x:
                x += step_x
                if self.piece_in_square((x,y)):
                    return True
        elif move[0] == 0: #vertical move
            while y != new_square[1]-step_y:
                y += step_y
                if self.piece_in_square((x,y)):
                    return True
        elif abs(move[0]) == abs(move[1]): #must be a diagonal move or a knight move
            while x != new_square[0]-step_x and y != new_square[1]-step_y:
                x, y = x + step_x, y + step_y
                if self.piece_in_square((x,y)):
                    return True

        return False

    def pick_random_move(self, poss_moves):
        num_pieces = len(poss_moves)
        #find randomm piece with more than zero moves
        rand_piece_move_list = []
        while len(rand_piece_move_list) == 0:
            rand_piece = random.choice(list(poss_moves))
            rand_piece_move_list = poss_moves[rand_piece]


        #get random move
        rand_move = random.choice(rand_piece_move_list)


        return rand_piece.coordinates, rand_move
        

if __name__ == '__main__':
    new_game = Game('Jon', 'CPU')
    new_game.game_loop()