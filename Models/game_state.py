import GUI

game_state = {
    'game': {
        'state': 'stopped', # paused, stopped, started
    },
    'config': {
        'starting_layout': '',
        'time_elapsed':'',
        'current_turn': '',
    },
    'black': {
        'player': '',
        'move_limit': '25',
        'time_limit': '',
        'score': '',
        'moves_taken': '',
        'move_time': '',
        'total_time': ''
    },
    'white': {
        'player': '',
        'move_limit': '25',
        'time_limit': '',
        'score': '',
        'moves_taken': '',
        'move_time': '',
        'total_time': ''
    }
}

black_move_history = []
white_move_history = []

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

def validate_text_input(context: GUI):
    for text_input in context.settings_inputs:
        if not text_input.get_value().isdigit():
            return False
    return True
