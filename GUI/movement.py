import copy

import GUI
from operator import itemgetter
from GUI import gui_updater
from Models import game_state
from Utility.constants import *
from Utility.enum import *

"""
A file to hold functions for game movement for AI
NOTE: Co ordinates should be in string format for easy board access ("I5")
NOTE: These moves do not include validation, which should be done prior to calling these functions
"""
def move_1_piece(context: GUI, old_coordinate, new_coordinate):
    old_tile = context.board.board_dict[old_coordinate]
    new_tile = context.board.board_dict[new_coordinate]

    temp = new_tile.piece
    new_tile.piece = old_tile.piece
    old_tile.piece = temp

def move_2_pieces(context: GUI, old_coordinate_1, old_coordinate_2, new_coordinate_1, new_coordinate_2):
    # The old coordinates should be sorted so that old_coordinate_2 is adjacent to new_coordinate1
    # Ex - Black moving (b2,c3) to (D4,C3)

    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]

    temp1 = new_tile_1.piece
    temp2 = new_tile_2.piece

    new_tile_1.piece = old_tile_1.piece
    new_tile_2.piece = old_tile_2.piece

    old_tile_1.piece = temp1
    old_tile_2.piece = temp2

def move_3_pieces(context: GUI, old_coordinate_1, old_coordinate_2, old_coordinate_3,
                  new_coordinate_1, new_coordinate_2, new_coordinate_3):
    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    old_tile_3 = context.board.board_dict[old_coordinate_3]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]
    new_tile_3 = context.board.board_dict[new_coordinate_3]

    temp1 = new_tile_1.piece
    temp2 = new_tile_2.piece
    temp3 = new_tile_3.piece

    new_tile_1.piece = old_tile_1.piece
    new_tile_2.piece = old_tile_2.piece
    new_tile_3.piece = old_tile_3.piece

    old_tile_1.piece = temp1
    old_tile_2.piece = temp2
    old_tile_3.piece = temp3

def sumito_two_to_one(context):
    pass

def sumito_three_to_one(context):
    pass

def sumito_three_to_two(context):
    pass

def push_two_to_one(context):
    pass

def push_three_to_one(context):
    pass

def push_three_to_two(context):
    pass




