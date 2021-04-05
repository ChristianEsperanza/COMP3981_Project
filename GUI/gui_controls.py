# Callback functions
import threading

import GUI
from GUI import movement, move_validation
from Models import game_state

"""
This is a collection of callback functions that are used in the GUI. This file functions mostly as a
callback bridge between the GUI buttons and the files that contain functions to carry out the 
desired action.
"""

def start_game_button(context: GUI):
    # game_state.start_game() will only return false if invalid inputs or game state
    if game_state.start_game(context) == False:
        context.update_printer("State or inputs invalid")
    else:
        context.update_printer(message="Starting game, white to move!")
        game_state.game_state['game']['state'] = 'started'
        context.start_timer()

def stop_game_button(context: GUI):
    if game_state.stop_game(context) == False:
        context.update_printer("Game is already stopped")
    else:
        context.update_printer("Stopping game")

def pause_game_button(context: GUI):
    if game_state.pause_game(context) == False:
        context.update_printer("Can't pause game")
    else:
        context.update_printer("Pausing game")
        game_state.game_state['game']['state'] = "paused"

def resume_game_button(context: GUI):
    if game_state.resume_game(context) == False:
        context.update_printer("Can't resume game")
    else:
        context.update_printer("Resuming game")

def reset_game_button(context: GUI):
    if game_state.reset_game(context) == False:
        context.update_printer("Can't reset game")
    else:
        context.update_printer("Resetting game")
        context.black_timer.reset_timer()
        context.white_timer.reset_timer()
    # context.board.build_board(context.window)

def undo_move_button(context: GUI):
    if game_state.undo_move(context) == False:
        context.update_printer("Can't undo move")
    else:
        context.update_printer("Undoing move")

##### Movement buttons #####
# Each button will first validate a move, then execute the move if valid.
# If the move is invalid, the pieces will be cleared

# TODO: This might be better off somewhere else
def check_movable_state():
    if game_state.game_state['game']['state'] == 'stopped':
        print("Game is stopped")
    elif game_state.game_state['game']['state'] == 'paused':
        print("Game is paused")
    else:
        return 1

def up_left_button(context: GUI):
    vector = (1, 0)
    if check_movable_state() == 1:
        # If valid then move
        if move_validation.is_valid(context, vector):
            movement.move_up_left(context)
        else:
            print("Invalid from gui_controls")