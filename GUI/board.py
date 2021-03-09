import pygame
import math
from GUI.tile import Tile
from Utility.constants import *

class Board:
    """
    Class which represents the board in the game window.
    """
    def __init__(self):
        self.board = []
        pass

    def build_board(self, window):
        self.set_default_tiles()
        self.update_board(window)
        pygame.display.update()

    def set_default_tiles(self):
        """
        Set the board for a Standard start.
        """
        self.board = [
            Tile(8, 4, "I5", white_piece_id), Tile(8, 5, "I6", white_piece_id), Tile(8, 6, "I7", white_piece_id), Tile(8, 7, "I8", white_piece_id), Tile(8, 8, "I9", white_piece_id),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", white_piece_id), Tile(7, 6, "H7", white_piece_id), Tile(7, 7, "H8", white_piece_id), Tile(7, 8, "H9", white_piece_id),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", white_piece_id), Tile(6, 5, "G6", white_piece_id), Tile(6, 6, "G7", white_piece_id), Tile(6, 7, "G8", None), Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None), Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None), Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", black_piece_id), Tile(2, 3, "C4", black_piece_id), Tile(2, 4, "C5", black_piece_id), Tile(2, 5, "C6", None), Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", black_piece_id), Tile(1, 3, "B4", black_piece_id), Tile(1, 4, "B5", black_piece_id), Tile(1, 5, "B6", black_piece_id),
            Tile(0, 0, "A1", black_piece_id), Tile(0, 1, "A2", black_piece_id), Tile(0, 2, "A3", black_piece_id), Tile(0, 3, "A4", black_piece_id), Tile(0, 4, "A5", black_piece_id),
        ]

    def set_german_daisy_tiles(self):
        """
        Set the board for a German Daisy start.
        """
        self.board = [
            Tile(8, 4, "I5", white_piece_id), Tile(8, 5, "I6", white_piece_id), Tile(8, 6, "I7", None), Tile(8, 7, "I8", black_piece_id), Tile(8, 8, "I9", black_piece_id),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", white_piece_id), Tile(7, 6, "H7", black_piece_id), Tile(7, 7, "H8", black_piece_id), Tile(7, 8, "H9", black_piece_id),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", white_piece_id), Tile(6, 4, "G5", white_piece_id), Tile(6, 5, "G6", None), Tile(6, 6, "G7", black_piece_id), Tile(6, 7, "G8", black_piece_id), Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None), Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None), Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", black_piece_id), Tile(2, 2, "C3", black_piece_id), Tile(2, 3, "C4", None), Tile(2, 4, "C5", white_piece_id), Tile(2, 5, "C6", white_piece_id), Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", black_piece_id), Tile(1, 3, "B4", white_piece_id), Tile(1, 4, "B5", white_piece_id), Tile(1, 5, "B6", white_piece_id),
            Tile(0, 0, "A1", black_piece_id), Tile(0, 1, "A2", black_piece_id), Tile(0, 2, "A3", None), Tile(0, 3, "A4", white_piece_id), Tile(0, 4, "A5", white_piece_id),
        ]

    def set_belgian_daisy_tiles(self):
        """
        Set the board for a Belgian Daisy start.
        """
        self.board = [
            Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None), Tile(8, 7, "I8", None), Tile(8, 8, "I9", None),
            Tile(7, 3, "H4", white_piece_id), Tile(7, 4, "H5", white_piece_id), Tile(7, 5, "H6", None), Tile(7, 6, "H7", None), Tile(7, 7, "H8", black_piece_id), Tile(7, 8, "H9", black_piece_id),
            Tile(6, 2, "G3", white_piece_id), Tile(6, 3, "G4", white_piece_id), Tile(6, 4, "G5", white_piece_id), Tile(6, 5, "G6", None), Tile(6, 6, "G7", black_piece_id), Tile(6, 7, "G8", black_piece_id), Tile(6, 8, "G9", black_piece_id),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", white_piece_id), Tile(5, 3, "F4", white_piece_id), Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", black_piece_id), Tile(5, 7, "F8", black_piece_id), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None), Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None), Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", black_piece_id), Tile(3, 2, "D3", black_piece_id), Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", white_piece_id), Tile(3, 6, "D7", white_piece_id), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", black_piece_id), Tile(2, 1, "C2", black_piece_id), Tile(2, 2, "C3", black_piece_id), Tile(2, 3, "C4", None), Tile(2, 4, "C5", white_piece_id), Tile(2, 5, "C6", white_piece_id), Tile(2, 6, "C7", white_piece_id),
            Tile(1, 0, "B1", black_piece_id), Tile(1, 1, "B2", black_piece_id), Tile(1, 2, "B3", None), Tile(1, 3, "B4", None), Tile(1, 4, "B5", white_piece_id), Tile(1, 5, "B6", white_piece_id),
            Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None), Tile(0, 3, "A4", None), Tile(0, 4, "A5", None),
        ]

    def update_board(self, window):
        """
        Updates the current board, going through the tiles and redrawing the
        images.
        NOTE: As of March 08, this should be fine to leave for the remainder of the
        project (barring geometry changes). Moves and tile changes should be handled
        outside of this method.
        """
        unoccupied = pygame.image.load('../COMP3981_Project/Images/unoccupied.png')
        black_stone_image = pygame.image.load('../COMP3981_Project/Images/resize_black.png')
        white_stone_image = pygame.image.load('../COMP3981_Project/Images/resize_white.png')

        # Iterate through columns, drawing a circle and adding the center point as a tuple to each Tile.
        # beginning has 25 X diff, end of row has a 40 X diff
        tile_counter = 0
        current_y = board_start_y + piece_radius
        for col in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            current_x = ((10 - col) * piece_radius) + piece_distance + board_start_x

            for row in range(0, col):
                if self.board[tile_counter].piece is None:
                    rect = window.blit(unoccupied, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)
                elif self.board[tile_counter].piece == white_piece_id:
                    rect = window.blit(white_stone_image, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)
                elif self.board[tile_counter].piece == black_piece_id:
                    rect = window.blit(black_stone_image, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)

                current_x += (piece_radius * 2) + piece_distance
                tile_counter += 1
            current_y += (piece_radius * 2) + piece_distance

    def swap_tiles(self, coord_a: tuple, coord_b: tuple):
        """
        Swaps the pieces of two tiles.
        :param coord_a: int
        :param coord_b: int
        """
        tile_a = None
        for tile in self.board:
            if tile.row == coord_a[0] and tile.column == coord_a[1]:
                tile_a = tile
                break
        tile_b = None
        for tile in self.board:
            if tile.row == coord_b[0] and tile.column == coord_b[1]:
                tile_b = tile
                break
        print(f"Swapping {tile_a.board_coordinate} and {tile_b.board_coordinate}")
        temp = tile_b.piece
        tile_b.piece = tile_a.piece
        tile_a.piece = temp


"""        
        # Iterate through columns, drawing a circle and adding the center point as a tuple to each Tile.
        # beginning has 25 X diff, end of row has a 40 X diff
        tile_counter = 0
        current_y = board_start_y + piece_radius
        for col in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            current_x = ((10 - col) * piece_radius) + piece_radius + board_start_x
            for row in range(0, col):
                # rect = window.blit(img, (current_x, current_y))
                # self.board[tile_counter].set_rect(rect)

                if self.board[tile_counter].piece is None:
                    rect = window.blit(unoccupied, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)
                elif self.board[tile_counter].piece == white_piece_id:
                    rect = window.blit(white_stone_image, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)
                elif self.board[tile_counter].piece == black_piece_id:
                    rect = window.blit(black_stone_image, (current_x, current_y))
                    self.board[tile_counter].set_rect(rect)

                current_x += (piece_radius * 2) + piece_distance
                tile_counter += 1
            current_y += (piece_radius * 2) + piece_distance

        # Dictionary of tiles - might be useful to explore later
        # tiles = {
        #     "I": [Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None), Tile(8, 7, "I8", None), Tile(8, 8, "I9", None)],
        #     "H": [Tile(7, 3, "H4", None), Tile(7, 4, "H5", None), Tile(7, 5, "H6", None), Tile(7, 6, "H7", None), Tile(7, 7, "H8", None), Tile(7, 8, "H9", None)],
        #     "G": [Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", None), Tile(6, 5, "G6", None), Tile(6, 6, "G7", None), Tile(6, 7, "G8", None), Tile(6, 8, "G9", None)],
        #     "F": [Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None)],
        #     "E": [Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None), Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None), Tile(4, 8, "E9", None)],
        #     "D": [Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None)],
        #     "C": [Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", None), Tile(2, 3, "C4", None), Tile(2, 4, "C5", None), Tile(2, 5, "C6", None), Tile(2, 6, "C7", None)],
        #     "B": [Tile(1, 0, "B1", None), Tile(1, 1, "B2", None), Tile(1, 2, "B3", None), Tile(1, 3, "B4", None), Tile(1, 4, "B5", None), Tile(1, 5, "B6", None)],
        #     "A": [Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None), Tile(0, 3, "A4", None), Tile(0, 4, "A5", None)]
        # }
        # [[tile.draw(window, len(tiles[x])) for tile in tiles[x]] for x in tiles.keys()]
"""


