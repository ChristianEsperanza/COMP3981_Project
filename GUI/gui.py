import thorpy
import pygame
import random

from GUI.board import Board
from Utility.constants import *
from Utility.enum import Vector
from Utility.enum import Turn
from operator import itemgetter


class GUI:
    """
    The Game class is the driver of the Abalone game. It initiates
    the setup to open a window and run the game.
    """

    def __init__(self):
        """
        Initialize GUI with empty window and console, which are to be built after the GUI is initialized
        """
        self.board = Board()
        self.window = None
        self.console = None
        self.selected_pieces = []
        self.player_turn = Turn.BLACK

    def run(self):
        """
        Builds the GUI and then runs the main loop, calling methods to build different pieces
        """
        # Build window, board, console
        self.build_window()
        self.board.build_board(self.window)
        self.build_console(self.window)
        event = None

        print(f"{self.player_turn.name} to move!")

        # TODO: Rename this function
        self.add_placeholders()

        pygame.display.set_caption("Abalone")
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    # for tile in self.board.board:
                    for key, tile in self.board.board_dict.items():
                        if tile.get_rect() is not None and tile.get_rect().collidepoint(pos):
                            print(f"Tile Coords: ({tile.row}, {tile.column})")
                            self.clicked_tile(tile)
                else:
                    self.handle_event(event, self.window)

            # self.dumb_stuff()
            self.console.react(event)
            pygame.display.update()

    def dumb_stuff(self):
        """
        Draws two flashing rectangles. Probably best we get rid of this.
        """
        rect = pygame.Rect(975, 450, 320, 450)
        pygame.draw.rect(self.window, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], rect)

        rect2 = pygame.Rect(1200, 0, 100, 450)
        pygame.draw.rect(self.window, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], rect2)


    def build_window(self):
        """
        Method to build the game window
        :return: Window
        """
        # Draw screen then game board
        window = pygame.display.set_mode((window_width, window_height))
        window.fill(blue)
        pygame.draw.rect(window, red, (0, 0, board_width, board_height))

        # Music
        # pygame.mixer.music.load('../COMP3981_project/Utility/yea.mp3')
        # pygame.mixer.music.set_volume(0.01)
        # pygame.mixer.music.play()

        self.window = window

    def build_console(self, window):
        """
        Builds the buttons and widgets to be displayed to the right of the board
        :param window:
        :return:
        """
        ####################################################################
        ###### Note: Most of this is broken or placeholder right now #######
        ####################################################################


        ########## STARTING POSITIONS DROPDOWN ##########
        # TODO: Requires fixing, crashes on selection
        starting_positions = [
            "Standard",
            "German Daisy",
            "Belgian Daisy"
        ]
        starting_position_dropdown = thorpy.DropDownListLauncher(const_text="Choose starting layout:",
                                                   var_text="",
                                                   titles=starting_positions)
        starting_position_dropdown.scale_to_title()
        starting_position_dropdown.set_size((button_length, button_height))

        ##########  CONTROLS BOX  ##########
        # TODO: These should call their actual functions
        start_button = thorpy.make_button("Start", func=self.test_func)
        start_button.set_size((button_length, button_height))
        stop_button = thorpy.make_button("Stop", func=self.test_func2)
        stop_button.set_size((button_length, button_height))
        pause_button = thorpy.make_button("Pause", func=self.test_func3)
        pause_button.set_size((button_length, button_height))
        reset_button = thorpy.make_button("Reset", func=self.test_func)
        reset_button.set_size((button_length, button_height))
        undo_button = thorpy.make_button("Undo", func=self.test_func)
        undo_button.set_size((button_length, button_height))

        controls_box = thorpy.Box.make(elements=[
            starting_position_dropdown, start_button, stop_button, pause_button, reset_button, undo_button
        ])

        controls_box.set_topleft((console_start_x, console_start_y))
        controls_box.set_size((225, 450))
        controls_box.blit()
        controls_box.update()

        ### SETTINGS ###
        black_settings_title = thorpy.make_text("Black", 22, (0,0,0))
        black_settings_title.set_size((button_length, button_height))

        black_move_limit = thorpy.make_button("Move Limit", func=self.test_func)
        black_move_limit.set_size((button_length, button_height))

        black_time_limit = thorpy.make_button("Time Limit", func=self.test_func)
        black_time_limit.set_size((button_length, button_height))

        black_human_computer_choice = thorpy.make_button("Human or AI", func=self.test_func)
        black_human_computer_choice.set_size((button_length, button_height))

        white_settings_title = thorpy.make_text("White", 22, (0,0,0))
        white_settings_title.set_size((button_length, button_height))

        white_move_limit = thorpy.make_button("Move Limit", func=self.test_func)
        white_move_limit.set_size((button_length, button_height))

        white_time_limit = thorpy.make_button("Time Limit", func=self.test_func)
        white_time_limit.set_size((button_length, button_height))

        white_human_computer_choice = thorpy.make_button("Human or AI", func=self.test_func)
        white_human_computer_choice.set_size((button_length, button_height))

        settings_box = thorpy.Box.make(elements=[
            black_settings_title, black_move_limit, black_time_limit, black_human_computer_choice,
            white_settings_title, white_move_limit, white_time_limit, white_human_computer_choice
        ])
        settings_box.set_topleft((console_start_x + 225, 0))
        settings_box.set_size((225, 450))
        settings_box.blit()
        settings_box.update()

        ######## MOVEMENT CONTROLS ########
        # Row 1
        up_left = thorpy.make_button("UP-L", func=self.test_func_move, params={"vector": Vector.UP_LEFT})
        up_left.set_size((50, 50))

        up_right = thorpy.make_button("UP-R", func=self.test_func_move, params={"vector": Vector.UP_RIGHT})
        up_right.set_size((50, 50))

        up_box = thorpy.Box([up_left, up_right])
        thorpy.store(up_box, mode="h")
        up_box.fit_children()

        # Row 2
        left = thorpy.make_button("<", func=self.test_func_move, params={"vector": Vector.LEFT})
        left.set_size((50, 50))

        center = thorpy.make_button("0", func=self.test_func_move)
        center.set_size((50, 50))
        center.set_topleft((2000, 1000))

        right = thorpy.make_button(">", func=self.test_func_move, params={"vector": Vector.RIGHT})
        right.set_size((50, 50))

        horiz_box = thorpy.Box([left, center, right])
        thorpy.store(horiz_box, mode="h")
        horiz_box.fit_children()

        # Row 3
        down_left = thorpy.make_button("DN-L", func=self.test_func_move, params={"vector": Vector.DOWN_LEFT})
        down_left.set_size((50, 50))

        down_right = thorpy.make_button("DN-R", func=self.test_func_move, params={"vector": Vector.DOWN_RIGHT})
        down_right.set_size((50, 50))
        down_right.stick_to(up_left, target_side="right", self_side="left")

        down_box = thorpy.Box([down_left, down_right])
        thorpy.store(down_box, mode="h")
        down_box.fit_children()

        move_box = thorpy.Box.make(elements=[up_box, horiz_box, down_box])
        move_box.set_topleft((console_start_x, 450))
        move_box.set_size((225, 450))
        move_box.blit()
        move_box.update()


        ########## CONSOLE BOX - Holds all groups ##########
        # Add to this
        elements = [controls_box]
        console_box = thorpy.Box.make(elements=elements)
        console_box.set_topleft((console_start_x, console_start_y))
        console_box.blit()
        console_box.update()

        self.console = thorpy.Menu([console_box, move_box])
        for element in self.console.get_population():
            element.surface = self.window

    def handle_event(self, event, window):
        # TODO: Flesh out, should handle most click events
        pos = pygame.mouse.get_pos()

    def clicked_tile(self, tile):
        # Deals with an event where a tile was clicked

        print(f"Clicked {tile.board_coordinate}, occupied by {tile.piece}")
        if tile not in self.selected_pieces:
            self.selected_pieces.append(tile)
            print(f"Added {tile.board_coordinate}")
        else:
            self.selected_pieces.remove(tile)
            print(f"Removed {tile.board_coordinate}")
        print([tile.board_coordinate for tile in self.selected_pieces])

    def test_func(self):
        # TODO: Delete this
        print("In test func")
        self.board.set_default_tiles()
        self.board.update_board(self.window)

    def test_func2(self):
        # TODO: Delete this
        print("Func 2")
        self.board.set_german_daisy_tiles()
        self.board.update_board(self.window)

    def test_func3(self):
        # TODO: Delete this
        print("func 3")
        self.board.set_belgian_daisy_tiles()
        self.board.update_board(self.window)

    def test_func_move(self, **kwargs):
        # print(f"{self.player_turn.name} to move!")
        print("Move: " + str(kwargs['vector']))
        vector_rep = kwargs['vector']

        try:

            vector = None
            selected_pieces_sorted = None

            # Moving of pieces. Sorting used for correct movement of pieces.
            if vector_rep == Vector.UP_LEFT:
                vector = (1, 0)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'), reverse=True)
            elif vector_rep == Vector.UP_RIGHT:
                vector = (1, 1)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'), reverse=True)
            elif vector_rep == Vector.LEFT:
                vector = (0, -1)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'))
            elif vector_rep == Vector.RIGHT:
                vector = (0, 1)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'), reverse=True)
            elif vector_rep == Vector.DOWN_LEFT:
                vector = (-1, -1)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'))
            elif vector_rep == Vector.DOWN_RIGHT:
                vector = (-1, 0)
                selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'))

            if self.is_valid_selection() and self.is_valid_move(vector_rep):

                # Swaps all tiles according to movement vector
                for tile in selected_pieces_sorted:
                    print(f"Moving vector {vector}")
                    self.board.swap_tiles((tile.row, tile.column), (tile.row + vector[0], tile.column + vector[1]))
                self.board.update_board(self.window)

                self.toggle_player_move()   # Other players turn.

            else:
                print("Invalid Move. Clearing selected pieces")

        except KeyError:
            print("Middle Button pressed")

        finally:
            self.selected_pieces.clear()

    def is_valid_selection(self):
        print("POG")
        if len(self.selected_pieces) > 3:
            return False
        prev_tile = None
        selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'))
        for tile in selected_pieces_sorted:
            print(tile)
            if tile.piece != self.player_turn.value:
                print("Wrong color")
                return False
            if prev_tile is not None:
                if prev_tile.row != tile.row or prev_tile.column != tile.column - 1:
                    print(f"{prev_tile.column}, {tile.column}")
                    print("Inconsistent row selection")
                    return False
                else:
                    prev_tile = tile
            else:
                prev_tile = tile
        return True

    def is_valid_move(self, vector_rep):
        board_seq = ('I5', 'I6', 'I7', 'I8', 'I9', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'G3', 'G4', 'G5', 'G6', 'G7',
                     'G8', 'G9', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
                     'E7', 'E8', 'E9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'C1', 'C2', 'C3', 'C4', 'C5',
                     'C6', 'C7', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'A1', 'A2', 'A3', 'A4', 'A5')
        for tile in self.selected_pieces:
            if tile.board_coordinate not in board_seq:
                print("Can't move out of bounds.")
                return False
        return True

    def toggle_player_move(self):
        if self.player_turn == Turn.WHITE:
            self.player_turn = Turn.BLACK
        else:
            self.player_turn = Turn.WHITE
        print(f"{self.player_turn.name} to move!")

    def add_placeholders(self):
        """
        Builds the boxes for black and white score, time taken,
        and moves taken
        """
        black_score_title = thorpy.make_text("Black", 22, (0,0,0))
        # black_score_title.set_size((button_length, button_height))

        black_time_title = thorpy.make_text("Time Taken: 0.0", 16, (0,0,0))
        black_moves_taken = thorpy.make_text("Moves Taken: 0", 16, (0,0,0))

        black_score_box  = thorpy.Box.make(elements=[
            black_score_title, black_time_title, black_moves_taken
        ])
        black_score_box.set_topleft((39, 663))
        black_score_box.blit()
        black_score_box.update()

        white_score_title = thorpy.make_text("White", 22, (0,0,0))
        white_time_title = thorpy.make_text("Time Taken: 0.0", 16, (0,0,0))
        white_moves_taken = thorpy.make_text("Moves Taken: 0", 16, (0,0,0))

        white_score_box  = thorpy.Box.make(elements=[
            white_score_title, white_time_title, white_moves_taken
        ])
        white_score_box.set_topleft((568, 663))
        white_score_box.blit()
        white_score_box.update()
