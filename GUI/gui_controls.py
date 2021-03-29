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
        print("Starting game, black to move!")

def stop_game_button(context: GUI):
    if game_state.stop_game(context) == False:
        print("Game is already stopped")
    else:
        print("Stopping game")

def pause_game_button(context: GUI):
    if game_state.pause_game(context) == False:
        print("Can't pause game")
    else:
        print("Pausing game")

def resume_game_button(context: GUI):
    if game_state.resume_game(context) == False:
        print("Can't resume game")
    else:
        print("Resuming game")

def reset_game_button(context: GUI):
    if game_state.reset_game(context) == False:
        print("Can't reset game")
    else:
        print("Resetting game")
    context.selected_pieces.clear()
    context.board.build_board(context.window)

def undo_move_button(context: GUI):
    if game_state.undo_move(context) == False:
        print("Can't undo move")
    else:
        print("Undoing move")
