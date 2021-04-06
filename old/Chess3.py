# So many iterations, but I think I found an efficient way.
# Every turn, we maintain a list of all 'capture squares' and 'move squares' for each player.
# We can simply check if a chosen move is in these lists, to see if its valid.
# Mainly, however, we can check checkmate very easily. If the player is in check, their valid moves must satisfy no longer being in check.
# If a player is in check, and there are no valid moves, it is checkmate.

from termcolor import colored

class Board:
    ranks = [1,2,3,4,5,6,7,8]
    files = ['a','b','c','d','e','f','g','h']

    def __init__(self):
        self.pieces = [Rook('white', (0,0)), Knight('white', (1,0)), Bishop('white',(2,0)), Queen('white',(3,0)), King('white', (4,0)), Bishop('white', (5,0)), Knight('white',(6,0)), Rook('white',(7,0)),
                        Pawn('white', (0,1)), Pawn('white', (1,1)), Pawn('white',(2,1)), Pawn('white',(3,1)),Pawn('white', (4,1)), Pawn('white', (5,1)), Pawn('white',(6,1)), Pawn('white',(7,1)),
                        Rook('black', (0,7)), Knight('black', (1,7)), Bishop('black',(2,7)), Queen('black',(3,7)), King('black', (4,7)), Bishop('black', (5,7)), Knight('black',(6,7)), Rook('black',(7,7)),
                        Pawn('black', (0,6)), Pawn('black', (1,6)), Pawn('black',(2,6)), Pawn('black',(3,6)),Pawn('black', (4,6)), Pawn('black', (5,6)), Pawn('black',(6,6)), Pawn('black',(7,6))]
        
        self.valid_moves = {} # a dictionary of piece : [valid_move]
        self.capture_moves = [] # a subset of valid moves?
    
    def move(self,old_coord, new_coord, player):
        self.update_valid_moves(player)
        if not self.piece_in_square(old_coord):
            raise ValueError("No piece in square to move from.")
        else:
            piece_to_move = self.get_piece(old_coord)
            move = new_coord[0] - old_coord[0], new_coord[1] - old_coord[1]
            if not player.colour == piece_to_move.colour:
                raise ValueError("Piece not of same colour.")
            else: #there exists a piece in the square we want to move from
                if self.piece_in_square(new_coord): # is there a piece in desired square?
                    capture = True
                else:
                    capture = False
                if not self.move_is_valid(piece_to_move, move):
                    raise ValueError("Piece is blocked.")
                else: # the move is not blocked
                    if capture:
                        player.points += self.capture_piece(piece_to_move, old_coord, new_coord)
                        print("Captured.")
                    self.move_piece(piece_to_move,old_coord, new_coord)

    def move_piece(self, p, old_coords, new_coords):
        '''
        Moves a piece to 'new_coords'. Updates piece's coordinates.
        '''
        #p =self.get_piece(old_coords)
        old_piece = self.get_piece(old_coords)
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
        
    def move_is_valid(self, p, m):
        print(p.coordinates)
        print(self.valid_moves[p])
        if m in self.valid_moves[p]:
            return True
        else:
            return False

    def update_valid_moves(self, player):
        for p in self.pieces:
            old_coord = p.coordinates

            for m in p.moveset:

                if player.colour ==  'white':
                    new_coord = p.coordinates[0] + m[0], p.coordinates[1] + m[1] #ensuring pawns go up or down depending on colour
                else:
                    new_coord = p.coordinates[0] - m[0], p.coordinates[1] - m[1]
                if new_coord[0] > 7 or new_coord[0] < 0 or new_coord[1] > 7 or new_coord[1] < 0:
                    pass
                else:
                    if self.valid_move(p,m, old_coord, new_coord):
                        if p not in self.valid_moves:
                            self.valid_moves[p] = []
                        self.valid_moves[p].append(new_coord)
            for c in p.capture_set:
                new_coord = p.coordinates[0] + c[0], p.coordinates[1] + c[1]
                if self.valid_move(p,c, old_coord, new_coord):
                    if new_coord not in self.valid_moves[p]:
                        self.valid_moves[p].append(new_coord)

    def valid_move(self,p, move, old_coord, new_coord):
        if not self.is_blocked(move, old_coord, new_coord):
            if self.piece_in_square(new_coord):
                blocking = self.get_piece(new_coord)
                if blocking.colour == p.colour:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

        return valid
    
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
            while x != new_square[0]-step_x and x > -1 and x < 9:
                x += step_x
                if self.piece_in_square((x,y)):
                    return True
        elif move[0] == 0: #vertical move
            while y != new_square[1]-step_y and y > -1 and y < 9:
                y += step_y
                if self.piece_in_square((x,y)):
                    return True
        elif abs(move[0]) == abs(move[1]): #must be a diagonal move or a knight move
            while x != new_square[0]-step_x and y != new_square[1]-step_y and x > -1 and x < 9 and y > -1 and y < 9:
                x, y = x + step_x, y + step_y
                if self.piece_in_square((x,y)):
                    return True

        return False
                
    def piece_in_square(self, coords):
        for p in self.pieces:
            if p.coordinates == coords:
                return True
        return False

    def get_piece(self, coords):
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

class Player():

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.points = 0
        self.in_check = False


    def update_points(self, piece_value):
        self.points += piece_value


    def __str__(self):
        return self.name

class Game:

    def __init__(self):
        pass

    def play(self):
        game_board = Board()

        player_1 = Player('Jon', 'white')
        player_2 = Player('CPU', 'black')


        to_play = player_1
        finished = False
        while not finished:
            print(to_play.name + ' (' + to_play.colour + ')' + " it is your go.")
            if to_play == player_1:
                opponent = player_2
            else:
                opponent = player_1
            # if to_play.in_check:
            #     if game_board.is_checkmate(to_play):
            #         print("You are in checkmate, GG")
            #         winner = opponent
            #         break
            #     else:
            #         print("You are in check. Move to get out of check.")

            #game_board.flip()
            print(game_board)
            
            moved = False
            while not moved:
                try:
                    sq1, sq2 = input('Enter squares: ').split(' ')
                    if sq1 == 'manual' and sq2 == 'checkmate':
                        finished = True
                        winner = opponent
                    
                    sq1 = self.square_to_coord(sq1)
                    sq2 = self.square_to_coord(sq2)

                    game_board.move(sq1, sq2, to_play)
                    print("Moved.")
                    moved = True
                except Exception as e: 
                    print("Invalid move, try again.")
                    print("Error was: " + str(e))
                    moved = False
            
            if to_play == player_1:
                to_play = player_2
            else:
                to_play = player_1

        print(str(winner) + " won with " + str(winner.points) + " points!")

    def square_to_coord(self, sq):
        try:
            file_ = sq[0]
            rank_ = int(sq[1])
            file_ = Board.files.index(file_)
            return file_, rank_-1
        except:
            raise ValueError("Invalid input.")
        

game = Game()
game.play()