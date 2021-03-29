import copy

import GUI
from GUI import gui_updater
from Utility.constants import *
from Utility.enum import *

game_state = {
    'game': {
        'state': 'stopped',  # paused, stopped, started
        'turn': 'black' # black, white
    },
    'config': {
        'starting_layout': '',
        'time_elapsed': '',
    },
    'black': {
        'player': '',  # human, AI
        'move_limit': '25',
        'time_limit': '',
        'score': 0,
        'moves_taken': 0,
        'move_time': '',
        'total_time': ''
    },
    'white': {
        'player': '',  # human, AI
        'move_limit': '25',
        'time_limit': '',
        'score': 0,
        'moves_taken': 0,
        'move_time': '',
        'total_time': ''
    }
}

# Add to the histories in the from-to format:
#   [a, b, c][x, y, z]
move_history_black = [[], []]
move_history_white = [[], []]
board_history = []

def start_game(context: GUI):
    # Can only start from a stopped position with valid text from inputs
    if game_state['game']['state'] != 'stopped' or not validate_text_input(context):
        return False
    else:
        # TODO: Fill in code for valid start position
        # Iterate through the GUI buttons and config, setting the configs as needed

        # Start timer
        pass

def pause_game(context: GUI):
    if game_state['game']['state'] == 'started':
        return True
    elif game_state['game']['state'] == 'paused':
        return False

def update_turn(context:GUI):
    game_state_copy = copy.copy(game_state)

    # Check for wins/no time left
    check_goal_state(context)

    # Add to board history then update
    board_history.append(context.board)
    context.board.update_board(context.window)

    # Update the GUI to account for the move/score/time, etc
    gui_updater.update_gui(context)

    # Calculate the current score after movement
    # TODO: Call this in functions where the score changes (IE sumitos)
    context.board.update_scores()

    # TODO: append move history

    # Go through each turn state (ie black/white and human/ai)  and check what the player config
    #   of the other player is. Update the current turn state to be the found config (ie human/ai).


    # Update the GUI:
    #   - Call context.update_turn_label(enum, )
    #   - Call context.update_score(enum, score from game_state)
    #   - Call context.update_moves_taken(enum)

    # Iterate through the state choices to find the current state, then:
    #   - Set the new game state/turn
    #   - Call context.toggle_player_move()
    #   - Reset turn timer to 0
    #   - Call the gui.update_time/moves/etc.

    if game_state['game']['turn'] == 'black':
        if game_state['black']['player'] == 'human':
            pass

    context.toggle_player_move()

def update_moves_taken(piece_enum):
    # Method which will be called after a move is finalized in game_board
    if piece_enum == Turn.WHITE:
        game_state['white']['moves_taken'] += 1
    if piece_enum == Turn.BLACK:
        game_state['black']['moves_taken'] += 1

def check_goal_state(context:GUI):
    # Check for a following goal state:
    #   - Win (6 points)
    #   - No time left on current player
    #   - No moves left on current player

    # Change state to stopped state

    # Print that b or w won

    pass

def validate_text_input(context: GUI):
    for text_input in context.settings_inputs:
        if not text_input.get_value().isdigit():
            return False
    return True

