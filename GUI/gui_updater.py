import GUI
from Models import game_state
from Utility.constants import *
from Utility.enum import *

"""
A collection of functions used to update the GUI using the game state.
NOTE: All of the attributes in game_state should be updated by the time these functions
are called. 
"""

def update_gui(context: GUI):
    update_gui_total_time(context)
    update_gui_move_time(context)
    update_gui_moves_taken(context)
    update_gui_turn_label(context)
    update_gui_score(context)

def update_gui_total_time(context: GUI, piece=None, move_time=None):
    if piece is None and move_time is None:
        context.update_total_time(Turn.WHITE, int(game_state.game_state['white']['total_time']))
        context.update_total_time(Turn.BLACK, int(game_state.game_state['black']['total_time']))
    else:
        if piece == Turn.WHITE:
            context.update_total_time(Turn.WHITE, int(move_time))
        else:
            context.update_total_time(Turn.BLACK, int(move_time))

def update_gui_move_time(context: GUI,  piece=None, move_time=None):
    if piece is None and move_time is None:
        context.update_turn_time(Turn.WHITE, int(game_state.game_state['white']['move_time']))
        context.update_turn_time(Turn.BLACK, int(game_state.game_state['black']['move_time']))
    else:
        if piece == Turn.WHITE:
            context.update_turn_time(Turn.WHITE, move_time)
        else:
            context.update_turn_time(Turn.BLACK, move_time)

def update_gui_moves_taken(context: GUI):
    context.update_moves_taken(Turn.WHITE, game_state.game_state['white']['moves_taken'])
    context.update_moves_taken(Turn.BLACK, game_state.game_state['black']['moves_taken'])

def update_gui_turn_label(context: GUI):
    if game_state.game_state['game']['turn'] == 'white':
        context.update_turn_label(Turn.WHITE)
    elif game_state.game_state['game']['turn'] == 'black':
        context.update_turn_label(Turn.BLACK)

def update_gui_score(context:GUI):
    context.update_score(Turn.WHITE, game_state.game_state['white']['score'])
    context.update_score(Turn.BLACK, game_state.game_state['black']['score'])
