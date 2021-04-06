import copy
from threading import Thread

import GUI
from AI import ai_main
from GUI import gui_updater
from Utility.constants import *
from Utility.enum import *

game_state = {
    'game': {
        'state': 'stopped',  # paused, stopped, started
        'turn': 'black'  # black, white
    },
    'config': {
        'starting_layout': '',  # default, german daisy, belgian daisy
        'time_elapsed': '',
    },
    'black': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': 0,
        'score': 0,
        'moves_taken': 0,
        'move_time': 0,
        'total_time': 0
    },
    'white': {
        'player': '',  # human, ai
        'move_limit': 0,
        'time_limit': 0,
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
        context.update_printer("Starting game, black to move!")
        set_game_config(context)
        context.start_timer()


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
        if game_state['turn'] == 'black' and game_state['black']['player'] == 'ai':
            context.update_printer("Black to move! AI is thinking...")
            ai_main.begin_turn(context, black_piece_id)

        elif game_state['turn'] == 'white' and game_state['white']['player'] == 'ai':
            context.update_printer("White to move! AI is thinking...")
            ai_main.begin_turn(context, white_piece_id)

        # TODO: Start the timer again


def reset_game(context: GUI):
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
    global game_state
    if game_state['game']['state'] != 'started' or len(board_history) < 2 or len(state_history) == 0:
        print("Can't undo")
        return False
    board_history.pop()
    last_board = board_history.pop()

    last_state = state_history.pop()
    last_state['game']['state'] == 'paused'
    game_state = copy.deepcopy(last_state)
    context.board = copy.deepcopy(last_board)

    context.toggle_player_move()
    gui_updater.update_gui(context)
    context.board.update_board(context.window)

    if game_state['game']['turn'] == 'black' and game_state['black']['player'] == 'ai':
        ai_main.begin_turn(context, black_piece_id)
    elif game_state['game']['turn'] == 'white' and game_state['white']['player'] == 'ai':
        ai_main.begin_turn(context, white_piece_id)


def update_turn(context: GUI):
    # Check for wins/no time left
    check_goal_state(context)

    # Add to board and state history then update
    temp_board = copy.deepcopy(context.board)
    temp_state = copy.deepcopy(game_state)

    board_history.append(temp_board)
    state_history.append(temp_state)
    context.board.update_board(context.window)

    # Calculate the current score after movement
    # TODO: Call this function in functions where the score changes (IE sumitos)
    context.board.update_scores()

    # TODO: append move history

    # Go through each turn state (ie black/white and human/ai) to find the correct state.
    # Once correct state is found, update the moves and time taken, update the state, and begin ai movement

    # If black just went
    if game_state['game']['turn'] == 'black':
        game_state['game']['turn'] = 'white'
        context.toggle_player_move()
        update_moves_taken(Turn.BLACK)
        gui_updater.update_gui(context)

        if game_state['white']['player'] == 'ai':
            context.update_printer("White to move! AI is thinking...")
            ai_main.begin_turn(context, white_piece_id)

        # else:
            # context.update_printer("White to move!")

    # If white just went
    elif game_state['game']['turn'] == 'white':
        game_state['game']['turn'] = 'black'
        context.toggle_player_move()
        update_moves_taken(Turn.WHITE)
        gui_updater.update_gui(context)

        if game_state['black']['player'] == 'ai':
            context.update_printer("Black to move! AI is thinking...")
            gui_updater.update_gui(context)
            ai_main.begin_turn(context, black_piece_id)

def update_moves_taken(piece_enum):
    # Method which will be called after a move is finalized in game_board
    if piece_enum == Turn.WHITE:
        game_state['white']['moves_taken'] += 1
    if piece_enum == Turn.BLACK:
        game_state['black']['moves_taken'] += 1


def check_goal_state(context: GUI):
    # Check for goal states before finalizing a turn
    #    Win (6 points)
    if game_state['white']['score'] == 6:
        game_state['game']['state'] = 'stopped'
        context.update_printer("White has won!")

    elif game_state['black']['score'] == 6:
        game_state['game']['state'] = 'stopped'
        context.update_printer("Black has won!")

    #    No moves left on current player
    elif game_state['white']['moves_taken'] == game_state['white']['move_limit']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("Black has won")

    elif game_state['black']['moves_taken'] == game_state['black']['move_limit']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("White has won")

    #    No time left on a player
    elif game_state['white']['time_limit'] == game_state['white']['total_time']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("Black has won")

    elif game_state['black']['time_limit'] == game_state['black']['total_time']:
        game_state['game']['state'] = 'stopped'
        context.update_printer("White has won")


def validate_text_input(context: GUI):
    for text_input in context.settings_inputs:
        if not text_input.get_value().isdigit():
            return False
    return True


def set_game_config(context: GUI):
    # Get the game configs from the GUI

    # Starting layout
    # TODO: Currently default layout  only, once dropdown is fixed adjust this
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

    # Set the turn state
    if game_state['black']['player'] == 'human':
        context.update_printer("Black to move!")
        game_state['game']['turn'] = 'black'
        game_state['game']['state'] = 'started'
        gui_updater.update_gui(context)

    elif game_state['black']['player'] == 'ai':
        game_state['game']['turn'] = 'black'
        game_state['game']['state'] = 'started'
        gui_updater.update_gui(context)

        context.update_printer("AI is thinking...")
        ai_main.begin_turn(context, black_piece_id)

    # gui_updater.update_gui(context)

def add_to_move_history(context: GUI, old_coordinates: list, new_coordinates:list):
    """
    Coordinates should come in a String list. Example:
    old_coordinates = ['I5', 'H4']
    new_coordinates = ['G3', 'H4']
    """
    if game_state['game']['turn'] == 'black':
        move_history_black[0].append(old_coordinates)
        move_history_black[1].append(new_coordinates)
        context.update_move_printer(f"Black moved from {old_coordinates} to {new_coordinates}")

    else:
        move_history_white[0].append(old_coordinates)
        move_history_white[1].append(new_coordinates)
        context.update_move_printer(f"White moved from {old_coordinates} to {new_coordinates}")
