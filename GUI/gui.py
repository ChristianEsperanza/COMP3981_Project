import pygame
import thorpy
from GUI.board import Board
from Utility.constants import *


class GUI:
    """
    The Game class is the driver of the Abalone game. It initiates
    the setup to open a window and run the game.
    """

    def __init__(self):
        self.board = Board()
        self.window = None
        self.console = None
        self.selected_pieces = []

    def run(self):
        """
        Builds the GUI and then runs the main loop calling methods to build different pieces
        """
        # Build window, board, console
        self.build_window()
        self.board.build_board(self.window)
        self.build_console(self.window)

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
                        if tile.get_rect() is not None and tile.get_rect().collidepoint(pos):
                            self.clicked_tile(tile)
                else:
                    self.handle_event(event, self.window)

            self.console.react(event)
            pygame.display.update()

    def build_window(self):
        """
        Method to build the game window
        :return: Window
        """
        # Draw screen then game board
        window = pygame.display.set_mode((window_width, window_height))
        pygame.draw.rect(window, red, (0, 0, board_width, board_height))
        self.window = window

    def build_console(self, window):
        """
        Builds the buttons and widgets to be displayed to the right of the board
        :param window:
        :return:
        """
        ########## STARTING POSITIONS DROPDOWN ##########
        starting_positions = [
            "Standard",
            "German Daisy",
            "Belgian Daisy"
        ]
        starting_position_dropdown = thorpy.DropDownListLauncher(const_text="Choose starting layout:",
                                                   var_text="",
                                                   titles=starting_positions)
        starting_position_dropdown.scale_to_title()

        ##########  CONTROLS BOX  ##########
        # TODO: These should call individual functions
        start_button = thorpy.make_button("Start", func=self.test_func2)
        start_button.set_size((button_length, button_height))
        stop_button = thorpy.make_button("Stop", func=self.test_func)
        stop_button.set_size((button_length, button_height))
        pause_button = thorpy.make_button("Pause", func=self.test_func)
        pause_button.set_size((button_length, button_height))
        undo_button = thorpy.make_button("Reset", func=self.test_func)
        undo_button.set_size((button_length, button_height))

        controls_box = thorpy.Box.make(elements=[
            start_button, stop_button, pause_button, undo_button
        ])
        controls_box.set_topleft((console_start_x, console_start_y))
        controls_box.blit()
        controls_box.update()

        ########## CONSOLE BOX - Holds all groups ##########
        elements = [starting_position_dropdown, controls_box]
        console_box = thorpy.Box.make(elements=elements)
        console_box.set_topleft((console_start_x, console_start_y))
        console_box.blit()
        console_box.update()

        self.console = thorpy.Menu([console_box])
        for element in self.console.get_population():
            element.surface = self.window

    def handle_event(self, event, window):
        # TODO: Flesh out, should handle most click events
        pos = pygame.mouse.get_pos()

    def clicked_tile(self, tile):
        # print(f"Clicked {tile.board_coordinate}, occupied by {tile.piece}")
        if tile not in self.selected_pieces:
            self.selected_pieces.append(tile)
            print(f"Added {tile.board_coordinate}")
        else:
            self.selected_pieces.remove(tile)
            print(f"Removed {tile.board_coordinate}")
        print([tile.board_coordinate for tile in self.selected_pieces])


    def test_func(self):
        print("In test func")

    def test_func2(self):
        print("Func 2")
