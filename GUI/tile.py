import pygame
from Utility.constants import *


class Tile:
    """
    Class to represent a tile to be displayed on the board.
    """

    def __init__(self, row, column, board_coordinate, piece):
        """
        Constructor for the tile
        :param x_coordinate: int, x coordinate on the board
        :param y_coordinate: int, y coordinate on the board
        :param board_coordinate: str, named coordinate on the board
        :param piece: int, ID of the piece colour (1 for White, 2 for Black)
        """
        self.row = row
        self.column = column
        self.board_coordinate = board_coordinate
        self.piece = piece
        self.rect = None

    def set_rect(self, rect):
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
