class Board():
    def __init__(self,):
        self.a = ['R',0,0,0,0,0,0] #a1 is a rook
        self.b = ['N',0,0,0,0,0,0]
        self.c = ['B',0,0,0,0,0,0]
        self.d = ['Q',0,0,0,0,0,0]
        self.e = ['K',0,0,0,0,0,0]
        self.f = ['B',0,0,0,0,0,0]
        self.g = ['N',0,0,0,0,0,0]
        self.h = ['R',0,0,0,0,0,0]
        self.board = [self.a,self.b,self.c,self.d,self.e,self.f,self.g,self.h]

    def get_piece(self, file_, rank):
        if file_ == 'a':
            return self.a[rank]
        elif file_ == 'b':
            return self.b[rank]

    def __repr__(self):
        board_string = ''
        for file_ in self.board:
            for space in file_:
                board_string += file_[]

class Game():

    # files = {
    #     'a':0
    #     'b':1
    #     'c':2
    #     'd':3
    #     'e':4
    #     'f':5
    #     'g':6
    #     'h':7
    # }

    def play(self):
        game_board = Board()
        move = input("Move: ")
        file_ = move[0]
        rank_ = move[1]
        print("piece on", move, "is", game_board.get_piece(file_, int(rank_)-1))

g = Game()
g.play()