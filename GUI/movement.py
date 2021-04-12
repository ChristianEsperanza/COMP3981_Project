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

def sumito_two_to_one(context:GUI, old_coordinates, new_coordinates):
    # Coordinate will come in String of its location (Ex: 'I6')
    # Ex: E7F8 to G8H9

    current_piece = context.board.board_dict[old_coordinates[0]].piece
    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]
    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None

def sumito_three_to_one(context, old_coordinate_1, new_coordinate):
    """
    Only need to move the piece from the first starting coordinate to the last end coordinate
    """
    # 3-1 Sumito  (F4E3D2 -> E3D2C1) - Push C1 off
    old_tile = context.board.board_dict[old_coordinate_1]
    old_piece = old_tile.piece
    new_tile = context.board.board_dict[new_coordinate]

    old_tile.piece = None
    new_tile.piece = old_piece

def sumito_three_to_two(context: GUI, old_coordinate_1, old_coordinate_2, old_coordinate_3,
                  new_coordinate_1, new_coordinate_2, new_coordinate_3, eliminated_coordinate):
    """
    Only need to remove the piece from the first starting coordinate and place it where the last target
    coordinate is going to be
    """
    # Will always end up 3 pieces of one side, 1 piece other side
    # Get the tiles
    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    old_tile_3 = context.board.board_dict[old_coordinate_3]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]
    new_tile_3 = context.board.board_dict[new_coordinate_3]
    pushed_to_tile_1 = context.board.board_dict[eliminated_coordinate]

    # Get pieces
    opposing_piece = pushed_to_tile_1.piece
    old_piece_1 = old_tile_1.piece
    old_piece_2 = old_tile_2.piece
    old_piece_3 = old_tile_3.piece

    # Clear old tiles and place new pieces
    old_tile_1.piece = None
    old_tile_2.piece = None
    old_tile_3.piece = None
    new_tile_1.piece = old_piece_1
    new_tile_2.piece = old_piece_2
    new_tile_3.piece = old_piece_3
    pushed_to_tile_1.piece = opposing_piece

# def push_two_to_one(context,old_coordinate_1, old_coordinate_2, new_coordinate_1, new_coordinate_2, target_coordinate):
def push_two_to_one(context, old_coordinates, new_coordinates, enemy_end_coordinates):
    """
    """

    # IE D5D6 - D6D7w
    # Move new_coordinate_2 to target
    # Empty out old_coordinate1

    # Empty the furthest back starting coordinate
    # old_tile = context.board.board_dict[old_coordinate_1]
    # temp = old_tile.piece
    # old_tile.piece = None
    #
    # # Move the single piece to the target coordinate
    # new_coordinate_2_tile = context.board.board_dict[new_coordinate_2]
    # new_coordinate_2_piece = new_coordinate_2_tile.piece
    #
    # target_coordinate_tile = context.board.board_dict[target_coordinate]
    # target_coordinate_tile.piece = new_coordinate_2_piece
    #
    # # Place the piece
    # new_coordinate_2_tile.piece = temp

    current_piece = context.board.board_dict[old_coordinates[0]].piece
    enemy_piece = context.board.board_dict[enemy_end_coordinates[0]].piece
    empty_coordinates = [coord for coord in old_coordinates if coord not in new_coordinates]

    for coord in enemy_end_coordinates:
        context.board.board_dict[coord].piece = enemy_piece

    for coord in new_coordinates:
        context.board.board_dict[coord].piece = current_piece

    for coord in empty_coordinates:
        context.board.board_dict[coord].piece = None


def push_three_to_one(context, old_coordinate_1, old_coordinate_2, old_coordinate_3, new_coordinate_1,
                      new_coordinate_2, new_coordinate_3, pushed_coordinate):
    # Coordinate will come in String of its location (Ex: 'I6')
    # Ex - F3F4F5 -> F4F5F6 Push F7

    # Get the tiles
    old_tile_1 = context.board.board_dict[old_coordinate_1]
    old_tile_2 = context.board.board_dict[old_coordinate_2]
    old_tile_3 = context.board.board_dict[old_coordinate_3]
    new_tile_1 = context.board.board_dict[new_coordinate_1]
    new_tile_2 = context.board.board_dict[new_coordinate_2]
    new_tile_3 = context.board.board_dict[new_coordinate_3]
    pushed_to_tile = context.board.board_dict[pushed_coordinate]

    # Store pieces
    opposing_piece = new_tile_3.piece
    piece_1 = old_tile_1.piece
    piece_2 = old_tile_2.piece
    piece_3 = old_tile_3.piece

    # Remove pieces from empty tile and place pieces
    old_tile_1.piece = None
    new_tile_1.piece = piece_1
    new_tile_2.piece = piece_2
    new_tile_3.piece = piece_3
    pushed_to_tile.piece = opposing_piece


def push_three_to_two(context, start_coordinate_1,  start_coordinate_2,  start_coordinate_3,
                      end_coordinate_1, end_coordinate_2, end_coordinate_3,
                      pushed_coordinate_1, pushed_coordinate_2):
    # Coordinate will come in String of its location (Ex: 'I6')
    # Ex (C1C2C3 -> C2C3C4) Push (C4C5 -> C5C6)

    # Get the tiles
    old_tile_1 = context.board.board_dict[start_coordinate_1]
    old_tile_2 = context.board.board_dict[start_coordinate_2]
    old_tile_3 = context.board.board_dict[start_coordinate_3]
    new_tile_1 = context.board.board_dict[end_coordinate_1]
    new_tile_2 = context.board.board_dict[end_coordinate_2]
    new_tile_3 = context.board.board_dict[end_coordinate_3]
    pushed_to_tile_1 = context.board.board_dict[pushed_coordinate_1]
    pushed_to_tile_2 = context.board.board_dict[pushed_coordinate_2]

    # Store pieces
    opposing_piece_1 = new_tile_3.piece
    opposing_piece_2 = pushed_to_tile_1.piece
    piece_1 = old_tile_1.piece
    piece_2 = old_tile_2.piece
    piece_3 = old_tile_3.piece

    # Remove pieces from empty tile and place pieces
    old_tile_1.piece = None
    new_tile_1.piece = piece_1
    new_tile_2.piece = piece_2
    new_tile_3.piece = piece_3
    pushed_to_tile_1.piece = opposing_piece_1
    pushed_to_tile_2.piece = opposing_piece_2

