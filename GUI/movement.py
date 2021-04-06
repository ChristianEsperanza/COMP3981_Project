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

edge_coordinates = [
    "I5", "I6", "I7", "I8", "I9", "H9", "HG9", "F9", "E9", "D8", "C7",
    "B6", "A5", "A4", "A3", "A2", "A1", "B1", "C1", "D1", "E1", "F2",
    "G3", "H4"
]


def move_1_piece(context: GUI, old_coordinate, new_coordinate):
    """
    Move a single piece, no pushes
    Coordinate will come in String of its location (Ex: 'I6')
    """

    old_tile = context.board.board_dict[old_coordinate]
    new_tile = context.board.board_dict[new_coordinate]

    new_tile.piece = old_tile.piece
    old_tile.piece = None

    context.update_move_printer(old_coordinate + " " + new_coordinate)

def move_2_pieces(context: GUI, old_coordinate_1, old_coordinate_2, new_coordinate_1, new_coordinate_2):
    # Coordinate will come in String of its location (Ex: 'I6')

    # The old coordinates should be sorted so that old_coordinate_2 is adjacent to new_coordinate1
    # Ex - Black moving (b2,c3) to (D4,C3)

    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]

    # Store the old pieces
    temp1 = old_tile_1.piece
    temp2 = old_tile_2.piece

    # Empty the old tiles
    old_tile_1.piece = None
    old_tile_2.piece = None

    # Place pieces into new coordinates
    new_tile_1.piece = temp1
    new_tile_2.piece = temp2

def move_3_pieces(context: GUI, old_coordinate_1, old_coordinate_2, old_coordinate_3,
                  new_coordinate_1, new_coordinate_2, new_coordinate_3):
    # Coordinate will come in String of its location (Ex: 'I6')

    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    old_tile_3 = context.board.board_dict[old_coordinate_3]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]
    new_tile_3 = context.board.board_dict[new_coordinate_3]

    # Store old pieces
    temp_1 = old_tile_1.piece
    temp_2 = old_tile_2.piece
    temp_3 = old_tile_3.piece

    # Empty the old tiles
    old_tile_1.piece = None
    old_tile_2.piece = None
    old_tile_3.piece = None

    # Place pieces in the new positions
    new_tile_1.piece = temp_1
    new_tile_2.piece = temp_2
    new_tile_3.piece = temp_3

def sumito_two_to_one(context: GUI, old_coordinate_1, old_coordinate_2, new_coordinate_1, new_coordinate_2):
    # Coordinate will come in String of its location (Ex: 'I6')

    # Ex: E7, F8 to G8, H9

    # First coordinate will be empty because it's pushing
    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]

    temp1 = new_tile_1.piece
    temp2 = new_tile_2.piece

    new_tile_1.piece = old_tile_1.piece
    new_tile_2.piece = old_tile_2.piece
    old_tile_1.piece = None #Pushing two pieces


    # The two pieces will move to their new coordinates

    pass

def sumito_three_to_one(context):
    # Coordinate will come in String of its location (Ex: 'I6')

    pass

def sumito_three_to_two(context):
    # Coordinate will come in String of its location (Ex: 'I6')

    pass

def push_two_to_one(context):
    # Coordinate will come in String of its location (Ex: 'I6')

    pass

def push_three_to_one(context):
    # Coordinate will come in String of its location (Ex: 'I6')

    pass

def push_three_to_two(context):
    # Coordinate will come in String of its location (Ex: 'I6')

    pass




