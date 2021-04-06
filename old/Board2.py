#imports
from termcolor import colored, cprint

#I want a board that fully implements all of the functionality I will need in a chess game. That means, I can call Board.get_piece(coordinate) with something like 'e4' and it will return
# an object of that piece

class Board:
    ranks = ['1','2','3','4','5','6','7','8']
    files = ['a','b','c','d','e','f','g','h']

    #The board is composed of 16 pieces for each player, and 64 squares in total. I could represent this as a 2D array of all the pieces in the game, or a dictionary with each
    # square having it's own ID


    def __init__(self):
        #I opted for a implementation where I explicitly define squares with pieces, but squares that are not in the dictionary are empty. This means I have to do input checking,
        # since 'i10' is not a square, only empty.
        self.board = {
            #Ranks 1 and 2 (white's)
            'a1':Rook('white'),
            'b1':Knight('white'),
            'c1':Bishop('white'),
            'd1':Queen('white'),
            'e1':King('white'),
            'f1':Bishop('white'),
            'g1':Knight('white'),
            'h1':Rook('white'),

            'a2':Pawn('white'),
            'b2':Pawn('white'),
            'c2':Pawn('white'),
            'd2':Pawn('white'),
            'e2':Pawn('white'),
            'f2':Pawn('white'),
            'g2':Pawn('white'),
            'h2':Pawn('white'),

            #Ranks 8 and 7 (black)
            'a8':Rook('black'),
            'b8':Knight('black'),
            'c8':Bishop('black'),
            'd8':Queen('black'),
            'e8':King('black'),
            'f8':Bishop('black'),
            'g8':Knight('black'),
            'h8':Rook('black'),

            'a7':Pawn('black'),
            'b7':Pawn('black'),
            'c7':Pawn('black'),
            'd7':Pawn('black'),
            'e7':Pawn('black'),
            'f7':Pawn('black'),
            'g7':Pawn('black'),
            'h7':Pawn('black')

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
            
            old_coord = self.square_to_coord(old_square)
            new_coord = self.square_to_coord(new_square)

            diffx, diffy = new_coord[0]- old_coord[0], new_coord[1] - old_coord[1]
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
    

    def is_check(self, move, old_square, new_square, piece, target_piece, colour):
        # I hate this method, but it works
        # I think I could turn the loops into other methods, to reduce the space used.
        # Essentially, a list of 'line of sight pieces' is maintained. We find the king, and loop out from the king, looking at pieces on 
        # the horizontal and vertical ranks, that the king could potentially be captured by.
        # As soon as a piece is found, it is added and it stops looking (as any piece that can move horizontally and vertically (or diagonally) needs
        # line of sight, unlike a knight

        #TODO: Check that enemy knights are not attacking the new position (as the new position could be a king move)
        del self.board[old_square]
        self.board[new_square] = piece

        is_check = False
        king_square = self.get_square(King(colour))
        king_coordinates = self.square_to_coord(king_square)
        king_x = king_coordinates[0]
        king_y = king_coordinates[1]

        los_pieces = []

        #add first piece found in horizontal and vertical (positive and negative) line of sights
        for sqx in range(king_x +1, 8):
            if self.piece_in_square(self.coord_to_square((sqx, king_y))):
                los_pieces.append(self.coord_to_square((sqx, king_y)))
                break
        for sqx in range(king_x -1, -1, -1):
            if self.piece_in_square(self.coord_to_square((sqx, king_y))):
                los_pieces.append(self.coord_to_square((sqx, king_y)))
                break
        for sqy in range(king_y+1, 8):
            if self.piece_in_square(self.coord_to_square((king_x, sqy))):
                los_pieces.append(self.coord_to_square((king_x, sqy)))
                break
        for sqy in range(king_y-1, -1, -1):
            if self.piece_in_square(self.coord_to_square((king_x, sqy))):
                los_pieces.append(self.coord_to_square((king_x, sqy)))
                break
        #add diagonal line of sights
        pos_x, pos_y = king_x, king_y
        neg_x, neg_y = king_x, king_y
        while pos_x != 9 and pos_y != 9:
            pos_x += 1
            pos_y += 1
            if self.piece_in_square(self.coord_to_square((pos_x, pos_y))):
                los_pieces.append(self.coord_to_square((pos_x, pos_y)))
                break
        pos_x, pos_y = king_x, king_y
        neg_x, neg_y = king_x, king_y
        while pos_x != 9 and neg_y != -1:
            pos_x += 1
            neg_y -= 1
            if self.piece_in_square(self.coord_to_square((pos_x, neg_y))):
                los_pieces.append(self.coord_to_square((pos_x, neg_y)))
                break
        pos_x, pos_y = king_x, king_y
        neg_x, neg_y = king_x, king_y
        while neg_x != -1 and pos_y != 9:
            neg_x -= 1
            pos_y += 1
            if self.piece_in_square(self.coord_to_square((neg_x, pos_y))):
                los_pieces.append(self.coord_to_square((neg_x, pos_y)))
                break
        pos_x, pos_y = king_x, king_y
        neg_x, neg_y = king_x, king_y
        while neg_x != -1 and neg_y != -1:
            neg_x -= 1
            neg_y -= 1
            if self.piece_in_square(self.coord_to_square((neg_x, neg_y))):
                los_pieces.append(self.coord_to_square((neg_x, neg_y)))
                break

        # TODO: Add checks for all piece captures (i.e. check if any piece can now capture the king. This will only be true if opposing colour is moving.)
        knights = []
        if colour == 'white':
            colour_to_check = 'black'
        else:
            colour_to_check = 'white'
        for sq in self.board:
            if self.get_piece(sq).colour == colour_to_check and self.get_piece(sq).symbol == 'N':
                knights.append(self.get_piece(sq))
                knight_x = self.square_to_coord(sq)[0]
                knight_y = self.square_to_coord(sq)[1]
        #for each knight, for each move, will executing the move capture the king
        for k in knights:
            for m in k.moveset:
                if knight_x + m[0] == king_x and knight_y + m[1] == king_y:
                    is_check = True


        for square in los_pieces:
            hypo_move = king_x - self.square_to_coord(square)[0] , king_y - self.square_to_coord(square)[1]
            if not self.get_piece(square).colour == colour and hypo_move in self.get_piece(square).capture_set:
                is_check = True


        self.board[old_square] = piece
        del self.board[new_square]

        return is_check

    def is_blocked(self, move, old_square, new_square):
        current_square = old_square
        new_square = new_square
        current_coord = self.square_to_coord(current_square)
        new_coord = self.square_to_coord(new_square)

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
        x=current_coord[0]
        y = current_coord[1]
        if move[1] == 0: #horizontal move
            while x != new_coord[0]-step_x:
                x += step_x
                if self.piece_in_square(self.coord_to_square((x,y))):
                    return True
        elif move[0] == 0: #vertical move
            while y != new_coord[1]-step_y:
                y += step_y
                if self.piece_in_square(self.coord_to_square((x,y))):
                    return True
        elif abs(move[0]) == abs(move[1]): #must be a diagonal move or a knight move
            while x != new_coord[0]-step_x and y != new_coord[1]-step_y:
                x, y = x + step_x, y + step_y
                if self.piece_in_square(self.coord_to_square((x,y))):
                    return True
        else:
            return False

    def is_checkmate(self, player):
        pass

    def in_moveset(self, vector, piece):
        if vector in piece.moveset:
            return True
        else:
            return False
    
    def in_captureset(self, vector, piece):
        if vector in piece.capture_set:
            return True
        else:
            return False
    
    def get_square(self, piece):
        for square in self.board:
            if self.board[square].symbol == piece.symbol and self.board[square].colour == piece.colour:
                return square
        return None
    
    def square_to_coord(self, square):
        file_ = square[0]
        rank_ = int(square[1])
        file_ = self.files.index(file_)
        return file_, rank_-1
    
    def coord_to_square(self, coord):
        rank_ = coord[1] +1
        file_ = self.files[coord[0]]
        return str(file_) + str(rank_)

    def piece_in_square(self, square):
        if square in self.board:
            return True
        else:
            return False

    def get_piece(self, square):
        return self.board[square]
    
    def flip(self):
        self.ranks.reverse()

    # When I print the board, I will want it to show in the same way each time. My previous implementation 'flipped' the board depending on the player, but this functionality
    # can come later
    def __repr__(self):
        gb_string = ''
        color = 'blue'
        gb_string += '  a b c d e f g h\n'
        for r in range(0, len(self.ranks)):
            gb_string += self.ranks[r]
            for f in range(0, len(self.files)):
                if self.files[f]+self.ranks[r] not in self.board:
                    gb_string+= '  '
                else:
                    piece = self.board[self.files[f]+self.ranks[r]]
                    color = piece.colour
                    if color == 'black':
                        color = 'grey'
                    gb_string += ' ' +colored(str(self.board[self.files[f]+self.ranks[r]]), color) 
            gb_string+='\n'
        return gb_string
    
# I could either make a 'white pawn' and 'black pawn' class or just a 'piece' class instead. I like the middle ground between encapsulation and functionality. Here
# I can make pawns with the selected colour. The colour of the piece will only matter in checking things, and will not affect the functionality.
# If I made 'piece' then it would not be as effective. Pieces have different movesets and symbols (and colours) but movesets and symbols are more relevant to
# how the piece works.

class Pawn():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "p"
        self.value = 1

        self.moveset = [(0,1),(0,2), (0,-1), (0,-2)] 
        self.capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)]


    def __str__(self):

        return self.symbol

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
        return self.symbol
        
class Knight():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "N"
        self.moveset = [(1,2),(-1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1)]
        self.capture_set = self.moveset
        self.value = 3

    def __repr__(self):
        return self.symbol

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
        return self.symbol

class King():
    def __init__(self, colour):
        self.colour = colour
        self.symbol = "K"
        self.moveset = [(0,1), (1,1), (1,0), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
        self.capture_set = self.moveset
        self.value = 1000
    def __repr__(self):
        return self.symbol
    
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

if __name__ == "__main__":
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
                if sq1[0] not in Board.files or sq1[1] not in Board.ranks or sq2[0] not in Board.files or sq2[1] not in Board.ranks:
                    raise ValueError("Invalid coordinates.")

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


