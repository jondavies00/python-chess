from termcolor import colored
import random
import colorama

from chess_game.board import Board
from chess_game.pieces import create_queen

from chess_game.player import Player

from chess_game.helpers import update_possible_squares


# Game has the board, and the players
class Game:
    def __init__(self, white_name, black_name):
        # Inititialise game settings
        # room for additional parameters such as turn time etc
        self.game_board = Board()
        self.player_1 = Player(white_name, "white", True)
        self.player_2 = Player(black_name, "black", False)

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

            # UPDATE VALID MOVES
            self.update_player_moves(board, to_play, opponent)
            if to_play.in_checkmate(board, opponent):
                finished = True
                self.winner = opponent
                self.loser = to_play
                self.win_type = "checkmate"
                break
            poss_moves = []

            for piece in self.game_board.pieces:
                if piece.colour == to_play.colour:
                    poss_moves.extend(piece.possible_moves)
            # print(str(to_play),"'s possible moves: ", poss_moves)

            # Get player input
            while not moved:
                try:
                    if to_play.human:
                        sq1, sq2 = input("Enter squares: ").split(" ")

                        coord1 = self.square_to_coord(sq1)
                        coord2 = self.square_to_coord(sq2)
                    else:
                        coord1, coord2 = self.pick_random_move(poss_moves)
                        print(
                            "%s (AI) picked %s to %s."
                            % (
                                to_play.name,
                                self.coord_to_square(coord1),
                                self.coord_to_square(coord2),
                            )
                        )

                    self.move(coord1, coord2, board, to_play)

                    print("Moved. %s points = %i" % (str(to_play), to_play.points))
                    moved = True
                except Exception as e:
                    print("Invalid move, try again.")
                    print("Error was: " + str(e))
                    moved = False

            print(self.move_history)
            # UPDATE VALID MOVES AGAIN
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
        elif to_ not in piece_to_move.possible_moves:
            raise ValueError(
                "Move is not a valid move. Either path is blocked, same coloured piece exists at target square, or move results in self-check"
            )
        else:
            print("VALID MOVE")
            # from here, we assume the move is valid
            # if there is a piece where we are moving to, it has to be captured (as its a valid move)
            capture_piece = board.get_piece(to_)
            if capture_piece != None:
                board.remove_piece(capture_piece)
                player.update_points(capture_piece.value)
            # move it to the desired position
            self.game_board.move_piece(piece_to_move, to_)
            self.move_history.append(
                str(piece_to_move) + str(self.coord_to_square(to_))
            )
            if piece_to_move.symbol == "p" and (to_[1] == 7 or to_[1] == 0):
                self.promote_pawn(piece_to_move, board)

    def promote_pawn(self, pawn, board):
        promoted = create_queen(pawn.colour, pawn.coordinates)
        board.remove_piece(pawn)
        board.add_piece(promoted)

    def update_player_moves(self, board, player, opponent):
        update_possible_squares(board, player, opponent, True)

    def get_aftermatch_stats(self):
        winner_points = self.winner.points
        loser_points = self.loser.points
        winner_name = self.winner.name
        loser_name = self.loser.name
        if self.win_type == "checkmate":
            stat_string = "%s won by checkmating %s" % (winner_name, loser_name)
        elif self.win_type == "time":
            stat_string = "%s won on time." % winner_name
        elif self.win_type == "draw":
            stat_string = "Nobody won. Draw."

        stat_string += "\n%s points: %i\n%s points: %i\nThanks for playing!" % (
            winner_name,
            winner_points,
            loser_name,
            loser_points,
        )
        return stat_string

    def square_to_coord(self, sq):
        try:
            file_ = sq[0]
            rank_ = int(sq[1])
            file_ = Board.files.index(file_)
            return file_, rank_ - 1
        except:
            raise ValueError("Invalid input.")

    def coord_to_square(self, coord):
        try:
            file_ = coord[0]
            rank_ = coord[1]
            file_ = Board.files[file_]

            return file_ + str(rank_ + 1)

        except:
            raise ValueError("Invalid input.")

    def is_blocked(self, move, old_square, new_square):
        # If the move is a negative vector, we want to step down, and step up otherwise
        if move[0] > 0:
            step_x = 1
        else:
            step_x = -1
        if move[1] > 0:
            step_y = 1
        else:
            step_y = -1
        # ignore current square and new square
        x = old_square[0]
        y = old_square[1]
        if move[1] == 0:  # horizontal move
            while x != new_square[0] - step_x:
                x += step_x
                if self.piece_in_square((x, y)):
                    return True
        elif move[0] == 0:  # vertical move
            while y != new_square[1] - step_y:
                y += step_y
                if self.piece_in_square((x, y)):
                    return True
        elif abs(move[0]) == abs(move[1]):  # must be a diagonal move or a knight move
            while x != new_square[0] - step_x and y != new_square[1] - step_y:
                x, y = x + step_x, y + step_y
                if self.piece_in_square((x, y)):
                    return True

        return False

    def pick_random_move(self, poss_moves):
        # find randomm piece with more than zero moves
        print("Poss moves; %s", poss_moves)
        rand_move = None
        while not rand_move:
            rand_piece = random.choice(self.game_board.pieces)
            if set(rand_piece.possible_moves) & set(poss_moves):
                rand_move = random.choice(rand_piece.possible_moves)

        return rand_piece.coordinates, rand_move
