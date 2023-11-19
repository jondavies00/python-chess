from chess_game.board import Board


def transform_move(i, di, p_n):
    """
    Allows a move to either be added or subtracted to coordinate i
    """
    if p_n:
        return i + di
    else:
        return i - di


def simulate_move(piece, move):
    piece.coordinates += move


def rollback_move(piece, move):
    piece.coordinates -= move


def update_possible_squares(board: Board, player, opponent, check_for_check):
    """
    Updates the 'possible squares' dictionary for the player. The dictionary maps player's pieces to squares that
    those pieces can move to.

    param board: the game board
    param opponent: the player's opponent
    """

    ####
    # UPDATING POSSIBLE SQUARES
    # Loop through every piece of colour
    # Generate all the squares that the piece could reach given its moveset
    # This means no negative squares, and no squares with pieces already on them

    # Can check if piece can reach square too
    ####

    my_pieces = [mp for mp in board.pieces if mp.colour == player.colour]

    ## Black pawns will be moving up (oldsq needs to subtract the move if moving from black side)
    if player.colour == "white":
        modifier = True  # positive
    else:
        modifier = False  # negative

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

        if piece.symbol == "B":
            pass

        for m in list(
            set(piece.move_set + piece.capture_set)
        ):  # add two lists together, remove dupesa2
            new_x = transform_move(piece.coordinates[0], m[0], modifier)
            new_y = transform_move(piece.coordinates[1], m[1], modifier)
            desired_square = (new_x, new_y)

            if (
                piece.symbol == "K"
                and piece.possible_moves
                and desired_square in piece.possible_moves
            ):
                pass
            elif new_x > 7 or new_x < 0 or new_y > 7 or new_y < 0:
                pass
            elif board.is_blocked(piece.coordinates, desired_square):
                pass
            elif (
                board.piece_in_square(desired_square)
                and board.get_piece(desired_square).colour == player.colour
            ):
                pass
            # capturing with a white pawn -> must be a forward capture
            # if its a back capture, we cant allow
            elif piece.symbol == "p" and m[1] < 0:
                pass
            elif piece.symbol == "p" and m[1] < 0:
                pass
            # If there is an *enemy* *piece* in the desired square and it's a *capture move*
            elif (
                board.piece_in_square(desired_square)
                and board.get_piece(desired_square).colour != player.colour
                and m in piece.capture_set
            ):
                if player.in_check(board, opponent):
                    print(player.name, "is in check.")
                    if player.move_gets_self_out_of_check(
                        board, piece, desired_square, opponent
                    ):
                        print(
                            "A move gets me out of check: ",
                            str(piece),
                            str(piece.coordinates),
                            str(desired_square),
                        )
                        poss_moves.append(desired_square)
                    else:
                        pass

                elif check_for_check:
                    if not player.move_results_in_self_check(
                        board, piece, desired_square, opponent
                    ):
                        poss_moves.append(desired_square)
                    else:
                        print(player.colour, "looked at", piece.colour)
                        print(
                            "A move would result in self check: ",
                            str(piece),
                            str(piece.coordinates),
                            str(desired_square),
                        )
                        pass
                else:
                    poss_moves.append(desired_square)
            # If there is no piece in the desired square, and it's not a capture move
            elif not board.piece_in_square(desired_square) and m in piece.move_set:
                if player.in_check(board, opponent):
                    print(player.name, "is in check.")
                    if player.move_gets_self_out_of_check(
                        board, piece, desired_square, opponent
                    ):
                        print(
                            "A move gets me out of check: ",
                            str(piece),
                            str(piece.coordinates),
                            str(desired_square),
                        )

                        poss_moves.append(desired_square)
                    else:
                        pass
                elif check_for_check:
                    if not player.move_results_in_self_check(
                        board, piece, desired_square, opponent
                    ):
                        poss_moves.append(desired_square)
                    else:
                        print(player.colour, "looked at", piece.colour)
                        print(
                            "A move would result in self check: ",
                            str(piece),
                            str(piece.coordinates),
                            str(desired_square),
                        )
                else:
                    poss_moves.append(desired_square)
            else:
                pass

            piece.possible_moves = poss_moves

        # self.capture_squares[piece] = poss_captures
