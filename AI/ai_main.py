import GUI
from GUI import gui_updater, movement
from Models import game_state

def begin_turn(context: GUI):
    # movement.move_1_piece(context, "C3", "D4")
    movement.move_2_pieces(context, "B2", "C3", "D4", "C3")
    # movement.move_3_pieces(context, "A1", "B2", "C3", "D4", "C3", "B2")

    game_state.update_turn(context)
