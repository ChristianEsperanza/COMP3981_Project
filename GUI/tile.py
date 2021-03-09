import pygame
from Utility.constants import *


class Tile:
    """
    Class to represent a tile to be displayed on the board.
    """

    def __init__(self, row, column, board_coordinate, piece):
        """
        Constructor for the tile. Holds a row and column (Ex. 8, 4),
        board coordinate for representation (Ex. "I5"), and a piece. A piece
        is defined in Utility/constants.py:
            white_piece_id = 1
            black_piece_id = 2
            Unoccupied = None
        :param x_coordinate: int, x coordinate on the board
        :param y_coordinate: int, y coordinate on the board
        :param board_coordinate: str, named coordinate on the board
        :param piece: int, ID of the piece colour
        """
        self.row = row
        self.column = column
        self.board_coordinate = board_coordinate
        self.piece = piece
        self.rect = None

    def set_rect(self, rect):
        """
        Setter for rect.
        When a tile is set by the board, it is given an image Rect object which
        is used to detect mouseclicks.
        :param rect:
        :return:
        """
        self.rect = rect

    def get_rect(self):
        return self.rect

    def __getitem__(self, item):
        if item == 'row':
            return self.row
        elif item == 'column':
            return self.column
        elif item == 'board_coordinate':
            return self.board_coordinate
        else:
            raise KeyError("Invalid item selection")
