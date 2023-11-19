# Made up of pieces (pawns, rooks etc)
# functions to get piece at coordinate
# functions to change coordinates of pieces
from termcolor import colored

from chess_game.pieces import (
    BasePiece,
    create_white_pawn,
    create_black_pawn,
    create_white_bishop,
    create_black_bishop,
    create_white_knight,
    create_black_knight,
    create_white_king,
    create_black_king,
    create_white_queen,
    create_black_queen,
    create_white_rook,
    create_black_rook,
)


class Board:
    """
    Board is set up as a list of pieces. There are ranks and files too. Board can be printed, and flipped so whoever is playing
    can have a better view of the board.
    """

    ranks = [1, 2, 3, 4, 5, 6, 7, 8]
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def __init__(self):
        self.pieces: list[BasePiece] = [
            create_white_rook((0, 0)),
            create_white_knight((1, 0)),
            create_white_bishop((2, 0)),
            create_white_queen((3, 0)),
            create_white_king((4, 0)),
            create_white_bishop((5, 0)),
            create_white_knight((6, 0)),
            create_white_rook((7, 0)),
            create_white_pawn((0, 1)),
            create_white_pawn((1, 1)),
            create_white_pawn((2, 1)),
            create_white_pawn((3, 1)),
            create_white_pawn((4, 1)),
            create_white_pawn((5, 1)),
            create_white_pawn((6, 1)),
            create_white_pawn((7, 1)),
            create_black_rook((0, 7)),
            create_black_knight((1, 7)),
            create_black_bishop((2, 7)),
            create_black_queen((3, 7)),
            create_black_king((4, 7)),
            create_black_bishop((5, 7)),
            create_black_knight((6, 7)),
            create_black_rook((7, 7)),
            create_black_pawn((0, 6)),
            create_black_pawn((1, 6)),
            create_black_pawn((2, 6)),
            create_black_pawn((3, 6)),
            create_black_pawn((4, 6)),
            create_black_pawn((5, 6)),
            create_black_pawn((6, 6)),
            create_black_pawn((7, 6)),
        ]

    def move_piece(self, p, new_coords):
        """Moves a piece to 'new_coords' by updating the piece's coordinates."""
        p.coordinates = new_coords

    def capture_piece(self, p, new_coords):
        """Finds target piece, and returns its value."""
        for piece in self.pieces:
            if piece.coordinates == new_coords:
                captured = piece
                self.piece.remove(piece)
        return captured.value

    def piece_in_square(self, coords):
        """Return whether a piece exists at the given coordinate"""
        for p in self.pieces:
            if p.coordinates == coords:
                return True
        return False

    def get_piece(self, coords):
        """Returns the piece at given coordinates."""
        for p in self.pieces:
            if p.coordinates == coords:
                return p
        return None

    def find_piece(self, piece_symbol, piece_colour):
        """Find and return a piece, given its symbol and colour."""
        for piece in self.pieces:
            if piece.symbol == piece_symbol and piece.colour == piece_colour:
                return piece

    def remove_piece(self, piece):
        """Remove a piece from the board"""
        self.pieces.remove(piece)

    def add_piece(self, piece):
        self.pieces.append(piece)

    def is_blocked(self, old_square, new_square):
        """
        Takes the squares a piece wants to move from, and to, as well as its move and checks the squares between them.
        If any square has a piece in it then return true, otherwise false.
        Since blockable moves can only be diagonal, horizontal, or vertical, we only need to check these cases.

        Keyword arguments:\n
        old_square -- the square the piece is moving from\n
        new_square -- the square the piece is moving to

        Returns:\n
        A boolean value based on whether the path is blocked.
        """
        move = new_square[0] - old_square[0], new_square[1] - old_square[1]

        # If the move is a negative vector, we want to step down, and step up otherwise
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
            while (
                x != new_square[0] - step_x
            ):  # While the current x we are incrementing has not reached the square before the desired one
                x += step_x
                if self.piece_in_square((x, y)):
                    return True
        elif move[0] == 0:  # Vertical move
            while y != new_square[1] - step_y:
                y += step_y
                if self.piece_in_square((x, y)):
                    return True
        elif abs(move[0]) == abs(move[1]):  # Must be a diagonal move
            while x != new_square[0] - step_x and y != new_square[1] - step_y:
                x, y = x + step_x, y + step_y
                if self.piece_in_square((x, y)):
                    return True
        else:
            # If none of the others, the move must either be a single square, or a knight move. Either way we check if anything
            # is on that square in the 'valid move' section of the code.
            return False

    def flip(self):
        self.ranks.reverse()

    def __str__(self):
        gb_string = ""
        color = ""
        back_colour = ""

        even_rank = True
        even_file = True
        found_piece = None
        for r in self.ranks:
            gb_string += str(r) + ""
            for f in range(0, len(self.files)):
                if even_rank:
                    if even_file == 0:
                        back_color = "on_grey"  # switch to on_white
                    else:
                        back_color = "on_grey"
                else:
                    if even_file == 0:
                        back_color = "on_grey"
                    else:
                        back_color = "on_grey"  # switch to on_white

                for p in self.pieces:
                    if (p.coordinates) == (f, r - 1):
                        if p.colour == "black":
                            color = "blue"
                        else:
                            color = "white"
                        found_piece = p
                        break

                if found_piece != None:
                    gb_string += "|" + colored(str(p), color, back_color) + ""
                else:
                    if back_color == "on_white":  # switch to on_white
                        color = "grey"
                    else:
                        color = "white"
                    gb_string += colored("| ", color, back_color)
                found_piece = None

                even_file = not even_file
            even_rank = not even_rank

            gb_string += "|\n"
        gb_string += "  a b c d e f g h"
        return gb_string
