# Callback functions
import GUI
from Models import game_state

"""
This is a collection of callback functions that are used in the GUI. The game_state 
will do the majority of the leg work, so this file functions mostly as a bridge between 
the GUI and game_state.
"""

def start_game_button(context: GUI):
    # game_state.start_game() will only return false if invalid inputs or game state
    if game_state.start_game(context) == False:
        print(f"Can't start if the game is {game_state.game_state['game']['state']} or if the "
              f"text inputs are invalid")
    else:
        print("Starting game from controls")

def stop_game_button(context: GUI):
    print("Stopping game")

def pause_game_button(context: GUI):
    print("Pausing game")

def reset_game_button(context: GUI):
    print("Resetting game")
    context.selected_pieces.clear()
    context.board.build_board(context.window)

def undo_move_button(context: GUI):
    print("Undoing move")

def validate_config(context: GUI):
    # 1. Check that a layout has been selected

    # 2. Check Move limit is valid

    # 3. Check time limit is valid

    # 4. Check game is stopped
    return True