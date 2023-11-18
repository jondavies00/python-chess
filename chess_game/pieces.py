# Pieces have coordinates, colour, movesets, and capture sets
# Only pawns have movesets != capture sets


from dataclasses import dataclass


# @dataclass(frozen=True)
# class BasePiece:
#     colour: str
#     coordinates: tuple[int, int]
#     symbol: str
#     move_set: list[tuple]
#     capture_set: list[tuple]
#     value: int

#     def __repr__(self):
#         return self.symbol + '(' + str(self.coordinates) + ')'
    
#     def __str__(self):
#         return self.symbol

# def create_white_pawn(coordinates: tuple[int, int]):
#     return BasePiece(colour='white', coordinates=coordinates, symbol='p', value=1, move_set=[(0,1),(0,2)], capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)])
# def create_black_pawn(coordinates: tuple[int, int]):
#     return BasePiece(colour='black', coordinates=coordinates, symbol='p', value=1, move_set=[(0,1),(0,2)], capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)])



class Pawn:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "p"
        self.value = 1

        self.moveset = [(0,1),(0,2)] 
        self.capture_set = [(1,1),(1,-1),(-1,1),(-1,-1)]


    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

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
    
    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

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

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

class Bishop:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "B"
        self.moveset = [
                        (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)
                        ]
        self.capture_set = self.moveset
        self.value = 3

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'

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

    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'
    
class Queen:
    def __init__(self, colour, coordinates):
        self.colour = colour
        self.coordinates = coordinates
        self.symbol = "Q"
        self.moveset = [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7),
                        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), 
                        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0,-1), (0,-2), 
                        (0,-3), (0,-4), (0,-5), (0,-6), (0,-7), (-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)
                        ]
        self.capture_set = self.moveset
        self.value = 10
    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return self.symbol + '(' + str(self.coordinates) + ')'
