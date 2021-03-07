import pygame
import math
from GUI.tile import Tile
from Utility.constants import *

class Board:
    def __init__(self):
        self.tiles = []
        pass

    def build_board(self, window):
        # pygame.draw.rect(window, red, (board_start_x, board_start_y, board_width, board_height), board_height)
        # circ = pygame.draw.circle(window, green, (board_start_x + 50, board_start_y+ 50),  piece_radius)
        self.draw_tiles(window)
        pygame.display.update()

    def search_window_coordinates(self):
        res = False

    def draw_tiles(self, window):
        # TODO: resize the current white/black stone images in /Images and replace this with an empty image
        img = pygame.image.load('../COMP3981_Project/Images/black_stone.svg')
        self.tiles = [
            Tile(8, 4, "I5", None), Tile(8, 5, "I6", None), Tile(8, 6, "I7", None), Tile(8, 7, "I8", None), Tile(8, 8, "I9", None),
            Tile(7, 3, "H4", None), Tile(7, 4, "H5", None), Tile(7, 5, "H6", None), Tile(7, 6, "H7", None), Tile(7, 7, "H8", None), Tile(7, 8, "H9", None),
            Tile(6, 2, "G3", None), Tile(6, 3, "G4", None), Tile(6, 4, "G5", None), Tile(6, 5, "G6", None), Tile(6, 6, "G7", None), Tile(6, 7, "G8", None), Tile(6, 8, "G9", None),
            Tile(5, 1, "F2", None), Tile(5, 2, "F3", None), Tile(5, 3, "F4", None), Tile(5, 4, "F5", None), Tile(5, 5, "F6", None), Tile(5, 6, "F7", None), Tile(5, 7, "F8", None), Tile(5, 8, "F9", None),
            Tile(4, 0, "E1", None), Tile(4, 1, "E2", None), Tile(4, 2, "E3", None), Tile(4, 3, "E4", None), Tile(4, 4, "E5", None), Tile(4, 5, "E6", None), Tile(4, 6, "E7", None), Tile(4, 7, "E8", None), Tile(4, 8, "E9", None),
            Tile(3, 0, "D1", None), Tile(3, 1, "D2", None), Tile(3, 2, "D3", None), Tile(3, 3, "D4", None), Tile(3, 4, "D5", None), Tile(3, 5, "D6", None), Tile(3, 6, "D7", None), Tile(3, 7, "D8", None),
            Tile(2, 0, "C1", None), Tile(2, 1, "C2", None), Tile(2, 2, "C3", None), Tile(2, 3, "C4", None), Tile(2, 4, "C5", None), Tile(2, 5, "C6", None), Tile(2, 6, "C7", None),
            Tile(1, 0, "B1", None), Tile(1, 1, "B2", None), Tile(1, 2, "B3", None), Tile(1, 3, "B4", None), Tile(1, 4, "B5", None), Tile(1, 5, "B6", None),
            Tile(0, 0, "A1", None), Tile(0, 1, "A2", None), Tile(0, 2, "A3", None), Tile(0, 3, "A4", None), Tile(0, 4, "A5", None),
        ]

        # Iterate through columns, drawing a circle and adding the center point as a tuple to each Tile.
        # beginning has 25 X diff, end of row has a 40 X diff
        tile_counter = 0
        current_y = board_start_y + piece_radius
        for col in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            current_x = ((10 - col) * piece_radius) + piece_radius + board_start_x
            for row in range(0, col):
                rect = window.blit(img, (current_x, current_y))
                self.tiles[tile_counter].set_rect(rect)

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

