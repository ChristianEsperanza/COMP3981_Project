# Callback functions
import GUI

def start_game_button(context: GUI):
    print("starting game")

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

