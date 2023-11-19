"""
Player has colour, name, and possible moves they can choose
"""
from __future__ import annotations
from chess_game.helpers import update_possible_squares
from chess_game.helpers import transform_move
from chess_game.pieces import BasePiece


class Player:
    def __init__(self, name, colour, human):
        self.name = name
        self.colour = colour
        self.points = 0
        self.human = human
        # self.in_check = False
        # self.possible_squares = {}
        # self.capture_squares = {}

    def update_points(self, piece_value):
        self.points += piece_value

    def move_results_in_self_check(
        self, board, piece: BasePiece, desired_square, opponent: Player
    ):
        current_squares = piece.possible_moves

        # save prior coords
        before_coords = piece.coordinates
        # if a piece gets captured, we need to save it
        captured = board.get_piece(desired_square)
        # temporarily remove the piece

        if captured != None:
            if captured.symbol == "K":
                return False
            else:
                board.remove_piece(captured)

        # perform move
        piece.coordinates = desired_square
        # update opponent's possible move squares now we simulated the move
        update_possible_squares(board, self, opponent, False)
        in_check = self.in_check(board, opponent)
        piece.coordinates = before_coords
        if captured != None:
            board.add_piece(captured)
        # opponent.update_possible_squares(board, self, False)
        piece.possible_moves = current_squares
        return in_check

    def move_gets_self_out_of_check(
        self, board, piece: BasePiece, desired_square, opponent
    ):
        # save prior coords
        possible_squares = piece.possible_moves

        # save move squares
        before_coords = piece.coordinates

        # if a piece gets captured, we need to save it
        captured = board.get_piece(desired_square)
        # temporarily remove the piece, if its the king we know its a check
        if captured != None:
            if captured.symbol == "K":
                return False
            else:
                board.remove_piece(captured)
        # perform move
        piece.coordinates = desired_square

        # update opponent's possible move squares now we simulated the move
        update_possible_squares(board, self, opponent, self, False)
        # see if we are no longer in check
        no_longer_in_check = not self.in_check(board, opponent)
        # rollback changes
        piece.coordinates = before_coords
        if captured != None:
            board.add_piece(captured)

        # opponent.update_possible_squares(board, self, False)
        piece.possible_moves = possible_squares
        return no_longer_in_check

    def in_check(self, board, opponent):
        """
        Goes through the opponent's possible squares. If my king is in them, set 'check' to true
        """

        check = False
        king = board.find_piece("K", self.colour)
        king_pos = king.coordinates
        opponent_attacking_squares = king.possible_moves
        # print("Opponents possible moves: ", opponent_attacking_squares)
        # print("My king position: ", king_pos)
        if opponent_attacking_squares:
            if king_pos in opponent_attacking_squares:
                # print("check")
                check = True

        return check

    def in_checkmate(self, board, opponent):
        # If there are no possible moves, it is checkmate.
        checkmate = True
        for piece in board.pieces:
            if piece.colour == self.colour and not piece.possible_moves and checkmate:
                continue
            else:
                checkmate = False
                break

        return checkmate

    def __str__(self):
        return self.name
