# Pieces have coordinates, colour, movesets, and capture sets
# Only pawns have movesets != capture sets


from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Colour(str, Enum):
    BLACK = "black"
    WHITE = "white"


@dataclass
class BasePiece:
    colour: str
    coordinates: tuple[int, int]
    symbol: str
    move_set: list[tuple]
    capture_set: list[tuple]
    value: int

    possible_moves: Optional[list[tuple]] = None

    def __repr__(self):
        return self.symbol + "(" + str(self.coordinates) + ")"

    def __str__(self):
        return self.symbol


def create_pawn(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="p",
        value=1,
        move_set=[(0, 1), (0, 2)],
        capture_set=[(1, 1), (1, -1), (-1, 1), (-1, -1)],
    )


def create_rook(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="R",
        value=3,
        move_set=[
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, -1),
            (0, -2),
            (0, -3),
            (0, -4),
            (0, -5),
            (0, -6),
            (0, -7),
            (-1, 0),
            (-2, 0),
            (-3, 0),
            (-4, 0),
            (-5, 0),
            (-6, 0),
            (-7, 0),
        ],
        capture_set=[
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, -1),
            (0, -2),
            (0, -3),
            (0, -4),
            (0, -5),
            (0, -6),
            (0, -7),
            (-1, 0),
            (-2, 0),
            (-3, 0),
            (-4, 0),
            (-5, 0),
            (-6, 0),
            (-7, 0),
        ],
    )


def create_bishop(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="B",
        value=3,
        move_set=[
            (1, -1),
            (2, -2),
            (3, -3),
            (4, -4),
            (5, -5),
            (6, -6),
            (7, -7),
            (-1, 1),
            (-2, 2),
            (-3, 3),
            (-4, 4),
            (-5, 5),
            (-6, 6),
            (-7, 7),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (-1, -1),
            (-2, -2),
            (-3, -3),
            (-4, -4),
            (-5, -5),
            (-6, -6),
            (-7, -7),
        ],
        capture_set=[
            (1, -1),
            (2, -2),
            (3, -3),
            (4, -4),
            (5, -5),
            (6, -6),
            (7, -7),
            (-1, 1),
            (-2, 2),
            (-3, 3),
            (-4, 4),
            (-5, 5),
            (-6, 6),
            (-7, 7),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (-1, -1),
            (-2, -2),
            (-3, -3),
            (-4, -4),
            (-5, -5),
            (-6, -6),
            (-7, -7),
        ],
    )


def create_knight(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="N",
        value=3,
        move_set=[
            (1, 2),
            (-1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
        ],
        capture_set=[
            (1, 2),
            (-1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
        ],
    )


def create_queen(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="Q",
        value=10,
        move_set=[
            (1, -1),
            (2, -2),
            (3, -3),
            (4, -4),
            (5, -5),
            (6, -6),
            (7, -7),
            (-1, 1),
            (-2, 2),
            (-3, 3),
            (-4, 4),
            (-5, 5),
            (-6, 6),
            (-7, 7),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (-1, -1),
            (-2, -2),
            (-3, -3),
            (-4, -4),
            (-5, -5),
            (-6, -6),
            (-7, -7),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, -1),
            (0, -2),
            (0, -3),
            (0, -4),
            (0, -5),
            (0, -6),
            (0, -7),
            (-1, 0),
            (-2, 0),
            (-3, 0),
            (-4, 0),
            (-5, 0),
            (-6, 0),
            (-7, 0),
        ],
        capture_set=[
            (1, -1),
            (2, -2),
            (3, -3),
            (4, -4),
            (5, -5),
            (6, -6),
            (7, -7),
            (-1, 1),
            (-2, 2),
            (-3, 3),
            (-4, 4),
            (-5, 5),
            (-6, 6),
            (-7, 7),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (-1, -1),
            (-2, -2),
            (-3, -3),
            (-4, -4),
            (-5, -5),
            (-6, -6),
            (-7, -7),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, -1),
            (0, -2),
            (0, -3),
            (0, -4),
            (0, -5),
            (0, -6),
            (0, -7),
            (-1, 0),
            (-2, 0),
            (-3, 0),
            (-4, 0),
            (-5, 0),
            (-6, 0),
            (-7, 0),
        ],
    )


def create_king(colour: str, coordinates: tuple[int, int]):
    return BasePiece(
        colour=colour,
        coordinates=coordinates,
        symbol="K",
        value=1 * 10 ^ 6,
        move_set=[(0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)],
        capture_set=[
            (0, 1),
            (1, 1),
            (1, 0),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ],
    )


def create_white_pawn(coordinates: tuple[int, int]):
    return create_pawn(colour=Colour.WHITE, coordinates=coordinates)


def create_black_pawn(coordinates: tuple[int, int]):
    return create_pawn(colour=Colour.BLACK, coordinates=coordinates)


def create_white_bishop(coordinates: tuple[int, int]):
    return create_bishop(Colour.WHITE, coordinates=coordinates)


def create_black_bishop(coordinates: tuple[int, int]):
    return create_bishop(Colour.BLACK, coordinates=coordinates)


def create_white_bishop(coordinates: tuple[int, int]):
    return create_bishop(Colour.WHITE, coordinates=coordinates)


def create_black_bishop(coordinates: tuple[int, int]):
    return create_bishop(Colour.BLACK, coordinates=coordinates)


def create_white_knight(coordinates: tuple[int, int]):
    return create_knight(Colour.WHITE, coordinates=coordinates)


def create_black_knight(coordinates: tuple[int, int]):
    return create_knight(Colour.BLACK, coordinates=coordinates)


def create_white_rook(coordinates: tuple[int, int]):
    return create_rook(Colour.WHITE, coordinates=coordinates)


def create_black_rook(coordinates: tuple[int, int]):
    return create_rook(Colour.BLACK, coordinates=coordinates)


def create_white_queen(coordinates: tuple[int, int]):
    return create_queen(Colour.WHITE, coordinates=coordinates)


def create_black_queen(coordinates: tuple[int, int]):
    return create_queen(Colour.BLACK, coordinates=coordinates)


def create_white_king(coordinates: tuple[int, int]):
    return create_king(Colour.WHITE, coordinates=coordinates)


def create_black_king(coordinates: tuple[int, int]):
    return create_king(Colour.BLACK, coordinates=coordinates)
