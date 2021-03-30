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
        'starting_layout': '', # default, german daisy, belgian daisy
        'time_elapsed': '',
    },
    'black': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': '',
        'score': 0,
        'moves_taken': 0,
        'move_time': 0,
        'total_time': 0
    },
    'white': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': '',
        'score': 0,
        'moves_taken': 0,
        'move_time': 0,
        'total_time': 0
    }
}

# Add to the histories in the from-to format:
#   [a, b, c][x, y, z]
move_history_black = [[], []]
move_history_white = [[], []]
board_history = []
state_history = []

def start_game(context: GUI):
    # Can only start from a stopped position with valid text from inputs
    if game_state['game']['state'] != 'stopped' or not validate_text_input(context):
        return False
    else:
        # TODO: Fill in code for valid start position

        set_game_config(context)
        # Start timer


def stop_game(context: GUI):
    if game_state['game']['state'] == 'stopped':
        return False
    else:
        game_state['game']['state'] = 'stopped'

def pause_game(context: GUI):
    # Can only pause if game has started
    if game_state['game']['state'] != 'started':
        return False

    else:
        # Set state and reset move timer
        game_state['game']['state'] = 'paused'
        if game_state['game']['turn'] == 'black':
            game_state['black']['move_time'] = 0
        else:
            game_state['white']['move_time'] = 0

def resume_game(context: GUI):
    # Resuming the game will change the state to 'started'

    if game_state['game']['state'] != 'paused':
        return False
    else:
        game_state['game']['state'] = 'started'

        #TODO: Start the timer again

def reset_game(context: GUI):
    # TODO: Is there a scenario where user should not be able to reset?

    # Reset game state
    game_state['game']['state'] = 'stopped'
    game_state['game']['turn'] = 'black'
    game_state['config']['starting_layout'] = ''
    game_state['config']['time_elapsed'] = ''
    game_state['black']['player'] = ''
    game_state['black']['move_limit'] = 0
    game_state['black']['time_limit'] = ''
    game_state['black']['score'] = 0
    game_state['black']['moves_taken'] = 0
    game_state['black']['move_time'] = 0
    game_state['black']['total_time'] = 0
    game_state['white']['player'] = ''
    game_state['white']['move_limit'] = 0
    game_state['white']['time_limit'] = ''
    game_state['white']['score'] = 0
    game_state['white']['moves_taken'] = 0
    game_state['white']['move_time'] = 0
    game_state['white']['total_time'] = 0

    # Reset GUI
    context.selected_pieces.clear()
    context.board.build_board(context.window, 'default')
    context.set_scoreboard()

    # Clear histories
    move_history_black = [[], []]
    move_history_white = [[], []]
    board_history = []
    gui_updater.update_gui(context)

def undo_move(context: GUI):
    # TODO: This does not work
    global game_state
    if game_state['game']['state'] != 'started' or len(board_history) == 0 or len(state_history) == 0:
        return False

    last_board = board_history.pop()
    state = state_history.pop()

    context.board.set_board(last_board.board, last_board.board_dict)
    context.board.update_board(context.window)

    game_state = copy.deepcopy(state)
    gui_updater.update_gui(context)
    context.toggle_player_move()


def update_turn(context:GUI):
    # Check for wins/no time left
    check_goal_state(context)

    # Add to board and state history then update
    board_history.append(context.board)
    state_history.append(game_state)
    context.board.update_board(context.window)


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

    # Temporary, to be deleted later. This just changes the turn for now
    if game_state['game']['turn'] == 'black':
        update_moves_taken(Turn.BLACK)
        game_state['game']['turn'] = 'white'
    else:
        update_moves_taken(Turn.WHITE)
        game_state['game']['turn'] = 'black'

    gui_updater.update_gui(context)
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

def set_game_config(context: GUI):
    # Get the game configs from the GUI

    # Starting layout
    #TODO: Currently default layout  only, once dropdown is fixed adjust this
    for layout in context.layout_radio_choices:
        if not layout.get_value():
            continue
        if layout.get_text() == "Default":
            context.board.build_board(context.window, 'default')
            game_state['config']['starting_layout'] = 'default'

        elif layout.get_text() == "German Daisy":
            context.board.build_board(context.window, 'german_daisy')
            game_state['config']['starting_layout'] = 'german daisy'

        elif layout.get_text() == "Belgian Daisy":
            context.board.build_board(context.window, 'belgian_daisy')
            game_state['config']['starting_layout'] = 'belgian daisy'

    # Settings for black
    if context.black_human_radio.get_value():
        game_state['black']['player'] = 'human'
    else:
        game_state['black']['player'] = 'ai'
    game_state['black']['move_limit'] = int(context.settings_inputs[0].get_value())
    game_state['black']['time_limit'] = context.settings_inputs[1].get_value()

    # Settings for White
    if context.white_human_radio.get_value():
        game_state['white']['player'] = 'human'
    else:
        game_state['white']['player'] = 'ai'
    game_state['white']['move_limit'] = int(context.settings_inputs[2].get_value())
    game_state['white']['time_limit'] = context.settings_inputs[3].get_value()

    # Set the turn
    if game_state['white']['player'] == 'human':
        game_state['game']['turn'] = 'white'
        game_state['game']['state'] = 'started'
    # TODO: Add AI option
    gui_updater.update_gui(context)

