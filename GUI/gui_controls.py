# Callback functions
import threading

import pygame

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
        context.update_printer(message="Starting game, black to move!")
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
        context.white_timer.pause_timer_temp()
        context.black_timer.pause_timer_temp()


def resume_game_button(context: GUI):
    if game_state.resume_game(context) == False:
        context.update_printer("Can't resume game")
    else:
        context.update_printer("Resuming game")
    # if game_state.game_state['game']['turn'] == 'white':
    #     context.white_timer.start_timer()
    # else:
    #     context.black_timer.start_timer()
    context.resume_timer()
    context.start_timer()


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


def set_board_button(context: GUI):
    game_state.set_board_config(context)


def sheesh(context: GUI, repeat=1):
    # pygame.mixer.music.load('../COMP3981_project/Utility/sheesh.mp3')
    pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(repeat)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('../COMP3981_project/Utility/sheesh.mp3'))


def stop_music(self):
    #TODO: Fill in, low priority tho
    pass
    # pygame.mixer.music.stop()
    # pygame.mixer.Channel.stop()
