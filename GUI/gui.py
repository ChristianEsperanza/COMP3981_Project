import pygame

from GUI.board import Board
from Utility.constants import *


class GUI:
    """
    The Game class is the driver of the Abalone game. It initiates
    the setup to open a window and run the game.
    """

    def __init__(self):
        self.board = Board()
        pass

    def run(self):
        """
        Run builds the GUI, calling methods to build different pieces
        """
        # Build window and board
        window = self.build_window()
        self.board.build_board(window)

        pygame.display.set_caption("Abalone")
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for tile in self.board.board:
                        if tile.get_rect().collidepoint(pos):
                            print(f"Clicked {tile.board_coordinate}")
                else:
                    self.handle_event(event, window)


    def build_window(self):
        """
        Method to build the game window
        :return: Window
        """
        # Draw screen then game board
        window = pygame.display.set_mode((window_width, window_height))
        pygame.draw.rect(window, red, (0, 0, board_width, board_height))
        return window

    def handle_event(self, event, window):
        # TODO: Flesh out, should handle most click events
        pos = pygame.mouse.get_pos()




