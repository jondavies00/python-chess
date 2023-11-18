"""
Player has colour, name, and possible moves they can choose
"""
from chess_game.helpers import transform_move


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
            # do piece.possible_squares ?
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
