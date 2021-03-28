from termcolor import colored, cprint

class Board():

    def __init__(self):
        # Define board
        self.board = [
            # Our logical representation of the board
            [Piece('rook', 'white'), Piece('knight', 'white'), Piece('bishop', 'white'),  Piece('queen', 'white'), Piece('king', 'white'), Piece('bishop', 'white'), Piece('knight', 'white'), Piece('rook', 'white')],
            [Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white'), Piece('pawn','white')],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            [Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black'), Piece('pawn','black')],
            [Piece('rook', 'black'), Piece('knight', 'black'), Piece('bishop', 'black'),  Piece('king', 'black'), Piece('queen', 'black'), Piece('bishop', 'black'), Piece('knight', 'black'), Piece('rook', 'black')]
        ]

    # we might need to update the allowed moves for each piece
    def update_allowed_moves(self):
        pass

    def check_move(self, sel_piece_name, piece_location, new_location, to_play):
        move = new_location[0] - piece_location[0], new_location[1] - piece_location[1]
        if Board.piece_at_location(self, sel_piece_name, piece_location, to_play):
            if Board.in_moveset(self, self.board[piece_location[0]][piece_location[1]], move):
                Board.move_piece(self, sel_piece_name ,piece_location, new_location)
                print("piece moved")
                return True
        return False
                

            

    def piece_at_location(self, sel_piece, piece_location, colour):
        piece_row = piece_location[0]
        piece_file = piece_location[1]
        piece = self.board[piece_row][piece_file]
        if not (piece == "empty"):
            if piece.get_name() == sel_piece and piece.get_colour() == colour: # selected piece exists in location and colour is of player's
                print("piece at location")
                return True
        return False

    def in_moveset(self, piece, move):
        temp = piece.get_moveset()

        if move in piece.get_moveset():
            return True
        else:
            return False

    def is_space_occupied(self, space, colour):
        # if the space has a piece of the same colour, cannot move
        # if the space has a piece of a different colour, need to decide if can capture.
        if colour == 'white':
            
        pass

    def move_piece(self, piece_name, curr_loc, new_location):
        curr_x, curr_y = curr_loc
        new_x, new_y = new_location
        old_piece = self.board[curr_x][curr_y]
        self.board[curr_x][curr_y] = "empty"
        self.board[new_x][new_y] = old_piece
        

    def __repr__(self):
        board_string = ""
        for y in range(len(self.board)):
            board_string += str(y + 1) + '| '
            
            for x in range(len(self.board)):
                if self.board[y][x] == "empty":
                    board_string += " "
                elif self.board[y][x].get_colour() == 'white':
                    board_string += colored(self.board[y][x].get_symbol(), 'white', 'on_blue')
                elif self.board[y][x].get_colour() == 'black':
                    board_string += colored(self.board[y][x].get_symbol(), 'grey', 'on_blue')

                board_string += ' | '
   
            board_string+='\n'
        return board_string
    

class Piece():
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        
        # TODO: define movesets
        if self.name == 'pawn':
            self.symbol = 'p'
            self.value = 1
            if self.colour == 'white':
                self.moveset = [(1,0),(2,0)] # the pawn can only move y+1 or y+2
                self.captures = [(1,1),(1,-1)]
            if self.colour == 'black':
                self.moveset = [(-1,0), (-2,0)]
                self.captures = [(-1,1),(-1,-1)]
                
            
        
        elif self.name == 'rook':
            self.moveset = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),(0,-8),
                            (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),(-8,0)]
            
            #self.moveset = self.moveset * -1
            self.value = 5
            self.symbol = 'R'
        elif self.name == 'knight':
            self.moveset = [(1,2),(-1,2),(2,1),(2,-1)]
            self.value = 3 
            self.symbol = 'N'
        elif self.name == 'bishop':
            self.value = 3 
            self.symbol = 'B'
        elif self.name == 'queen':
            self.value = 10
            self.symbol = 'Q'
        elif self.name == 'king':
            self.value = 10**10
            self.symbol = 'K'
        
    
    def get_colour(self):
        return self.colour
    def get_name(self):
        return self.name
    def get_symbol(self):
        return self.symbol
    def get_moveset(self):
        return self.moveset
    
class Game():

    symbol_to_piece_name = {
        'p' : 'pawn',
        'B': 'bishop',
        'R': 'rook',
        'N': 'knight',
        'Q': 'queen',
        'K': 'king'
    }

    notation_to_coordinate = {
        'a':0,
        'b':1,
        'c':2,
        'd':3,
        'e':4,
        'f':5,
        'g':6,
        'h':7
    }

    def start_game(self):
        #....
        my_board = Board()
        game_ended = False
        to_play = 'white'
        while not game_ended:
            print(my_board)
            if to_play == 'white':
                print('White to move... ')
            elif to_play == 'black':
                print('Black to move... ')
            valid = False
            while not valid:
                    
                piece, old_loc, new_loc = self.decode_move(input("ENTER MOVE (notation: (piece symbol) (location) (new_location), use 'p' for pawn): ")) #e.g. a2 a3 to move pawn to a3
                valid = my_board.check_move(piece, old_loc, new_loc, to_play)
                print("your move was: ", piece, old_loc, new_loc)

                if valid == False:
                    print("Invalid move, try again.")

            if to_play == 'white':
                to_play = 'black'
            elif to_play == 'black':
                to_play = 'white'
            print(to_play)
        #....
            
    
    def valid_move(self, sel_piece, old_loc, new_loc, game_board, to_play):
        return game_board.check_move(sel_piece, old_loc, new_loc, to_play)

    def decode_move(self, move):
        #moves will be a simplified notation where player inputs 'movefrom' square and 'moveto'
        piece_symbol, move_from, move_to = move.split(' ')
        old_loc = 0,0
        new_loc = 0,0

        piece_name = Game.symbol_to_piece_name[piece_symbol]
        old_loc =  int(move_from[1]) -1 ,Game.notation_to_coordinate[move_from[0]] #e.g. a4 gets converted to 0, 3
        new_loc = int(move_to[1]) -1 , Game.notation_to_coordinate[move_to[0]]
        return piece_name, old_loc, new_loc


new_game = Game()

new_game.start_game()