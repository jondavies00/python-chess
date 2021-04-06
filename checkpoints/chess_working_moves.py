from termcolor import colored
# made up of pieces (pawns, rooks etc)
# functions to get piece at coordinate
# functions to change coordinates of pieces
class Board:
    ranks = [1,2,3,4,5,6,7,8]
    files = ['a','b','c','d','e','f','g','h']

    def __init__(self):
        self.pieces = [Rook('white', (0,0)), Knight('white', (1,0)), Bishop('white',(2,0)), Queen('white',(3,0)), King('white', (4,0)), Bishop('white', (5,0)), Knight('white',(6,0)), Rook('white',(7,0)),
                        Pawn('white', (0,1)), Pawn('white', (1,1)), Pawn('white',(2,1)), Pawn('white',(3,1)),Pawn('white', (4,1)), Pawn('white', (5,1)), Pawn('white',(6,1)), Pawn('white',(7,1)),
                        Rook('black', (0,7)), Knight('black', (1,7)), Bishop('black',(2,7)), Queen('black',(3,7)), King('black', (4,7)), Bishop('black', (5,7)), Knight('black',(6,7)), Rook('black',(7,7)),
                        Pawn('black', (0,6)), Pawn('black', (1,6)), Pawn('black',(2,6)), Pawn('black',(3,6)),Pawn('black', (4,6)), Pawn('black', (5,6)), Pawn('black',(6,6)), Pawn('black',(7,6))]
    
    def move_piece(self, p, new_coords):
        '''
        Moves a piece to 'new_coords' by updating the piece's coordinates.
        '''
        p.coordinates = new_coords

    def capture_piece(self, p, old_coords, new_coords):
        '''
        Finds target piece, and returns its value
        '''
        for piece in self.pieces:
            if piece.coordinates == new_coords:
                captured = piece
                self.piece.remove(piece)
        return captured.value

    def piece_in_square(self, coords):
        for p in self.pieces:
            if p.coordinates == coords:
                return True
        return False

    def get_piece(self, coords):
        '''
        Returns the piece at given coordinates.
        param coords: the coordinates of the piece you would like
        '''
        for p in self.pieces:
            if p.coordinates == coords:
                return p
        return None

    def flip(self):
        self.ranks.reverse()

    def __str__(self):
        gb_string = ''
        color = ''
        gb_string += '  a b c d e f g h\n'
        found_piece = None
        for r in range(0, len(self.ranks)):
            gb_string += str(self.ranks[r]) + ' '
            for f in range(0, len(self.files)):
                for p in self.pieces:

                    if (p.coordinates) == (f,r):
                        if p.colour == 'black':
                            color = 'grey'
                        else:
                            color = 'white'
                        found_piece = p
                        break
                        
                if found_piece != None :
                    gb_string += colored(str(p), color) + ' '
                else: 
                    gb_string+= '  '
                found_piece = None

            gb_string+='\n'
        return gb_string


# Pieces have coordinates, colour, movesets, and capture sets
# Only pawns have movesets != capture sets

class Pawn:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "p"
        self.value = 1

        self.moveset = [(0,1),(0,2), (0,-1), (0,-2)] 
        self.capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)]


    def __str__(self):
        return self.symbol

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

class Bishop:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "B"
        self.moveset = [
                        (0, 0), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __str__(self):
        return self.symbol

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
    
class Queen:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "Q"
        self.moveset = [(0, 0), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
                        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0,-1), (0,-2), 
                        (0,-3), (0,-4), (0,-5), (0,-6), (0,-7), (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 10
    def __str__(self):
        return self.symbol


# Player has colour, name, and possible moves they can choose
class Player():

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.points = 0
        self.in_check = False
        self.possible_squares = {}


    def update_points(self, piece_value):
        self.points += piece_value

    def update_possible_squares(self, board):
        if self.colour == 'white':
            pass
        else:
            pass

    def __str__(self):
        return self.name

# Game has the board, and the players
class Game:

    def __init__(self, white_name, black_name):
        # Inititialise game settings
        # room for additional parameters such as turn time etc
        self.game_board = Board()
        self.player_1 = Player(white_name, 'white')
        self.player_2 = Player(black_name, 'black')

        self.finished = False

    def game_loop(self):
        to_play = self.player_1
        while not self.finished:
            print(str(to_play) + " it is your go.")
            print(self.game_board)


            moved = False

            #Get player input
            while not moved:
                try:
                    sq1, sq2 = input('Enter squares: ').split(' ')

                    sq1 = self.square_to_coord(sq1)
                    sq2 = self.square_to_coord(sq2)
                    #UPDATE VALID MOVES
                    self.move(sq1, sq2, self.game_board, to_play)

                    print("Moved.")
                    moved = True
                except Exception as e: 
                    print("Invalid move, try again.")
                    print("Error was: " + str(e))
                    moved = False

            if to_play == self.player_1:
                to_play = self.player_2
            else:
                to_play = self.player_1
    
    def move(self, from_, to_, board, player):
        # TODO: CHECK MOVE IS VALID (I.E. IN PLAYERS POSSIBLE MOVES)

        # __________________________________________________________

        #from here, we assume the move is valid

        # get the piece we want to move
        piece_to_move = board.get_piece(from_)
        # move it to the desired position
        self.game_board.move_piece(piece_to_move, to_)


    def update_player_moves(self):
        self.player_1.update_possible_squares()
        self.player_2.update_possible_squares()    

    def square_to_coord(self, sq):
        try:
            file_ = sq[0]
            rank_ = int(sq[1])
            file_ = Board.files.index(file_)
            return file_, rank_-1
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


if __name__ == '__main__':
    new_game = Game('Jon', 'CPU')
    new_game.game_loop()