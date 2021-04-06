import _thread
import threading
from threading import Thread

import GUI
from AI.Evaluator import Evaluator
from GUI import gui_updater, movement
from Models import game_state
from Utility.constants import *

def begin_turn(context: GUI, piece_id):
    execute_thread(context, piece_id)

def execute_thread(context:GUI, piece_id):
    _thread.start_new_thread(calculate, (context, piece_id))

def calculate(context:GUI, piece_id):
    board_state = context.board.to_string_state()
    turn = ('b', 'w')[piece_id == white_piece_id]
    best_move = Evaluator.minimax(board_state, turn)
    find_and_execute_move(best_move, context)

    game_state.update_turn(context)


def find_and_execute_move(best_move, context: GUI):
    """
    param: best_move: list[str]
    If the best move is to move a single piece, then it will come in
    best_move will come in list with each string being a joined value of the coordinate
    and the colour.
    Ex - ['C3b','C4w']
    """
    start_coordinates = best_move['start']
    end_coordinates = best_move['end']

    # Breaks down the object retrieved from the evaluator and executes the move


    # Is the move a sumito?
    if best_move['elim'] == True:
        pass

    # Will the move push other pieces?
    elif best_move['pushes'] > 0:
        print("hello")
        pass

    # Move to new coordinates
    else:
        # If not the above, then it is a simple movement
        # Start/end coordinates are string if 1 move, list otherwise
        if isinstance(start_coordinates, str):
            movement.move_1_piece(context, strip_coordinate(start_coordinates), strip_coordinate(end_coordinates))
            game_state.add_to_move_history(context, [start_coordinates], [end_coordinates])

        elif len(start_coordinates) == 2:
            movement.move_2_pieces(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]),
                                   strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]))
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        elif len(start_coordinates) == 3:
            movement.move_3_pieces(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]), strip_coordinate(start_coordinates[2]),
                                   strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]), strip_coordinate(end_coordinates[2]))
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)


def strip_coordinate(move_string):
    # Strip the colour from a given coordinate
    return move_string[0] + move_string[1]

