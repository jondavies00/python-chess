from termcolor import colored
class Board:

    ranks = ['1','2','3','4','5','6','7','8']
    files = ['a','b','c','d','e','f','g','h']

    def __init__(self):
        self.board = {
            (0,0):Rook('white'),
            (1,0):Knight('white'),
            (2,0):Bishop('white'),
            (3,0):Queen('white'),
            (4,0):King('white'),
            (5,0):Bishop('white'),
            (6,0):Knight('white'),
            (7,0):Rook('white'),

            (0,1):Pawn('white'),
            (1,1):Pawn('white'),
            (2,1):Pawn('white'),
            (3,1):Pawn('white'),
            (4,1):Pawn('white'),
            (5,1):Pawn('white'),
            (6,1):Pawn('white'),
            (7,1):Pawn('white'),

            #Ranks 8 and 7 (black)
            (0,6):Pawn('black'),
            (1,6):Pawn('black'),
            (2,6):Pawn('black'),
            (3,6):Pawn('black'),
            (4,6):Pawn('black'),
            (5,6):Pawn('black'),
            (6,6):Pawn('black'),
            (7,6):Pawn('black'),

            (0,7):Rook('black'),
            (1,7):Knight('black'),
            (2,7):Bishop('black'),
            (3,7):Queen('black'),
            (4,7):King('black'),
            (5,7):Bishop('black'),
            (6,7):Knight('black'),
            (7,7):Rook('black')
        }
    
    def move(self, old_square, new_square, current_player, opponent):
        '''
        Move takes the old square, and new square, and checks many parameters
        to ensure the move is valid.
        returns: error if invalid move, 0 if no capture, piece value if capture
        '''
        #0. Is a piece in the selected square?
        if not self.piece_in_square(old_square):
            raise ValueError("No piece in square")
        else:
            piece = self.board[old_square]
            diffx, diffy = new_square[0]- old_square[0], new_square[1] - old_square[1]
            #1. Is piece of correct colour?
            if piece.colour == current_player.colour:
                #2. Is the target coordinate empty?
                if not self.piece_in_square(new_square):
                    exists_target_piece = False
                    target_piece = None
                    #3. Is move in the moveset?
                    if not self.in_moveset((diffx, diffy), piece):
                        raise ValueError("Move not in moveset")

                else:
                    target_piece = self.board[new_square]
                    exists_target_piece = True
                    #A piece is at the target coordinate
                    #4. Is move in capture set?
                    if not self.in_captureset((diffx, diffy), piece):
                        raise ValueError("Move not in capture set")
                    if target_piece.colour == current_player.colour:
                        raise ValueError("Same colour piece in target square.")

                #Can piece get to square?
                if not self.is_blocked((diffx, diffy), old_square, new_square):
                    # The piece can get to the square, and the move is valid

                    #Ensure we don't put ourselves in check.
                    if not self.is_check((diffx, diffy), old_square, new_square, piece, target_piece, current_player.colour):
                        # Did we put opponent in check?
                        if self.is_check((diffx, diffy), old_square, new_square, piece, target_piece, opponent.colour):
                            opponent.in_check = True
                            print("CHECK")
                        else:
                            opponent.in_check = False
                        del self.board[old_square]
                        self.board[new_square] = piece
                        if exists_target_piece:
                            return target_piece.value
                        else:
                            return 0
                    else:
                        raise ValueError("Move results in self-check")
                else:
                    raise ValueError("Move blocked")
            else:
                raise ValueError("Not your piece")

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

    def in_moveset(self, vector, piece):
        if vector in piece.moveset:
            return True
        else:
            return False

    def piece_in_square(self, square):
        if square in self.board:
            return True
        else:
            return False

    def flip(self):
        self.ranks.reverse()

    def __repr__(self):
        gb_string = ''
        color = 'blue'
        gb_string += '  a b c d e f g h\n'
        for r in range(0, len(self.ranks)):
            gb_string += self.ranks[r]
            for f in range(0, len(self.files)):
                if (f,r) not in self.board:
                    gb_string+= '  '
                else:
                    piece = self.board[(f,r)]
                    color = piece.colour
                    if color == 'black':
                        color = 'grey'
                    gb_string += ' ' +colored(str(self.board[(f,r)]), color) 
            gb_string+='\n'
        return gb_string

class Pawn:
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "p"
        self.value = 1

        self.moveset = [(0,1),(0,2), (0,-1), (0,-2)] 
        self.capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)]


    def __str__(self):

        return self.symbol

class Rook:
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
        return self.symbol
        
class Knight:
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "N"
        self.moveset = [(1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1)]
        self.capture_set = self.moveset
        self.value = 3

    def __repr__(self):
        return self.symbol

class Bishop:
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
        return self.symbol

class King:
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "K"
        self.moveset = [(0,1), (1,1), (1,0), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        self.capture_set = self.moveset
        self.value = 1000
    def __repr__(self):
        return self.symbol
    
class Queen:
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
        return self.symbol

class Player():

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.points = 0
        self.in_check = False
        self.possible_moves = []

    def update_points(self, piece_value):
        self.points += piece_value
    
    def update_move_list(self, board):
        pieces = board.get_pieces(self.colour)
        


    def __str__(self):
        return self.name

class Game:

    def __init__(self):
        pass

    def play(self):
        game_board = Board()
        game_board.flip()
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
            if to_play.in_check:
                if game_board.is_checkmate(to_play):
                    print("You are in checkmate, GG")
                    winner = opponent
                    break
                else:
                    print("You are in check. Move to get out of check.")

            game_board.flip()
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

                    to_play.points += game_board.move(sq1, sq2, to_play, opponent)
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
        


g = Game()
g.play()
