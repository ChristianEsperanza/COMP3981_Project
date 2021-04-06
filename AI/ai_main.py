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
    Function to find the type of move (Sumito, push, or move) and call the correct movement function.
    If the best move is to move a single piece, then it will come in
    best_move will come in list with each string being a joined value of the coordinate
    and the colour.
    Ex - ['C3b','C4w']
    """
    start_coordinates = best_move['start']
    end_coordinates = best_move['end']
    pushes = best_move['pushes']
    #
    # sorted_start_coordinates = [context.board.board_dict[strip_coordinate(coord)] for coord in start_coordinates]
    # sorted_end_coordinates = [context.board.board_dict[strip_coordinate(coord)] for coord in end_coordinates]
    # if not isinstance(start_coordinates, str):
    #     sorted_start_coordinates = context.sort_selected_pieces(movement_to_vector_enum(best_move['move']), start_coordinates)
    #     sorted_end_coordinates = context.sort_selected_pieces(movement_to_vector_enum(best_move['move']), end_coordinates)

    # Start/end coordinates are a string if 1 move, list otherwise

    # Pushing and sumito
    if pushes > 0:
        # Two marbles pushing
        if len(start_coordinates) == 2:
            # Sumito two to one
            if best_move['elim']:
                movement.sumito_two_to_one(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]),
                                                            strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]))
                game_state.add_to_move_history(context, start_coordinates, end_coordinates)

            # Push two to one
            else:
                # IE D5D6 - D6D7w
                vector = best_move['move'].value
                target_coordinate = get_next_coordinate(end_coordinates[1], vector)

                movement.push_two_to_one(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]),
                                        strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]), target_coordinate)
                game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        # 3-1 Push    (C3C4C5 -> C4C5C6)
        # 3-2 Sumito  (F6F5F4 -> F5F4F3) - Push F2
        # 3-1 Sumito  (F4E3D2 -> E3D2C1) - Push C1
        # 3-2 Sumito  (E5F6G7 -> F6G7H8) - Push I9

        # Three marbles pushing
        if len(start_coordinates) == 3:
            if best_move['elim']:
                vector = best_move['move'].value

                # Sumito 3-1
                # Should be fine as is
                if pushes == 1:
                    movement.sumito_three_to_one(context, strip_coordinate(start_coordinates[0]), strip_coordinate(end_coordinates[2]))
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

                # Sumito 3-2
                else:

                    # (D3D4D5) -> (D2D3D4) Pushed off d1
                    pushed_coordinate = get_next_coordinate(strip_coordinate(end_coordinates[2]), vector)
                    movement.sumito_three_to_two(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]), strip_coordinate(start_coordinates[2]),
                                                 strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]), strip_coordinate(end_coordinates[2]),
                                                 pushed_coordinate)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

            else:

                vector_tuple = best_move['move'].value

                # Push 3-1
                if pushes == 1:
                    pushed_coordinate = get_next_coordinate(strip_coordinate(end_coordinates[2]), vector_tuple)
                    movement.push_three_to_one(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]), strip_coordinate(start_coordinates[2]),
                                               strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]),
                                               strip_coordinate(end_coordinates[2]), pushed_coordinate)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

                # Push 3-2
                else:
                    # TODO: Pushing left/right doesn't work correctly every time
                    # Ex - (G6G7G8 -> G5G6G7) Pushed (G5G4 -> G4G3)
                    pushed_coordinate_1 = get_next_coordinate(strip_coordinate(end_coordinates[2]), vector_tuple)
                    pushed_coordinate_2 = get_next_coordinate(pushed_coordinate_1, vector_tuple)

                    movement.push_three_to_two(context,
                                               strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]),strip_coordinate(start_coordinates[2]),
                                               strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]), strip_coordinate(end_coordinates[2]),
                                               pushed_coordinate_1, pushed_coordinate_2)
                    game_state.add_to_move_history(context, start_coordinates, end_coordinates)

    # If not pushing, move to designated coordinates
    else:
        # Move one stone
        # Start/end coordinates come in strings instead of list in this situation
        if isinstance(start_coordinates, str):
            movement.move_1_piece(context, strip_coordinate(start_coordinates), strip_coordinate(end_coordinates))
            game_state.add_to_move_history(context, [start_coordinates], [end_coordinates])

        # Move two stones
        elif len(start_coordinates) == 2:
            movement.move_2_pieces(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]),
                                   strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]))
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)

        # Move three stones
        elif len(start_coordinates) == 3:
            movement.move_3_pieces(context, strip_coordinate(start_coordinates[0]), strip_coordinate(start_coordinates[1]), strip_coordinate(start_coordinates[2]),
                                   strip_coordinate(end_coordinates[0]), strip_coordinate(end_coordinates[1]), strip_coordinate(end_coordinates[2]))
            game_state.add_to_move_history(context, start_coordinates, end_coordinates)

def get_next_coordinate(last_coordinate: str, vector: tuple):
    return f"{chr(ord(last_coordinate[0]) + vector[0])}{int(last_coordinate[1]) + vector[1]}"

def strip_coordinate(move_string):
    # Strip the colour from a given coordinate
    return move_string[0] + move_string[1]

