import thorpy
import pygame
import random

from GUI import gui_controls
from GUI.board import Board
from Utility.constants import *
from Utility.enum import Vector
from Utility.enum import Turn
from operator import itemgetter
from GUI.gui_controls import *

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
        self.build_console()
        self.draw_score_and_time()
        self.set_scoreboard()
        event = None

        print(f"{self.player_turn.name} to move!")

        pygame.display.set_caption("Abalone")
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                # GUI buttons react to event
                self.console.react(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    for key, tile in self.board.board_dict.items():
                        if tile.get_rect() is not None and tile.get_rect().collidepoint(pos):
                            print(f"Tile Coords: ({tile.row}, {tile.column})")
                            self.clicked_tile(tile)
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

    def build_console(self):
        """
        Builds the buttons and widgets to be displayed to the right of the board
        The process of adding elements is as follows:
            1. Create desired elements (button, text, etc.)
            2. Make a new thorPy Box and add the new elements to the box
            3. Set the size and position of the box
            4. Call blit() then update() at the bottom of this function so other
                elements are not overwritten
            5. Add the box to self.console at the bottom of this function.
        """
        # TODO: Requires fixing, crashes on selection
        starting_position_title = thorpy.make_text("Starting Position", 18, (0,0,0))
        starting_position_title.set_size((button_length, button_height))


        starting_positions = [
            "Standard",
            "German Daisy",
            "Belgian Daisy"
        ]
        # starting_positions = [
        #     ("Standard", self.board.set_default_tiles()),
        #     ("German Daisy", self.board.set_german_daisy_tiles()),
        #     ("Belgian Daisy", self.board.set_belgian_daisy_tiles())
        # ]
        starting_position_dropdown = thorpy.DropDownListLauncher(const_text="Choose starting layout:",
                                                                 var_text="",
                                                                 titles=starting_positions)
        starting_position_dropdown.scale_to_title()
        starting_position_dropdown.set_size((button_length, button_height))

        ##########  CONTROLS BOX  ##########
        start_button = thorpy.make_button("Start", func=lambda: gui_controls.start_game_button(self))
        start_button.set_size((button_length, button_height))

        stop_button = thorpy.make_button("Stop", func=lambda: gui_controls.stop_game_button(self))
        stop_button.set_size((button_length, button_height))

        pause_button = thorpy.make_button("Pause", func=lambda: gui_controls.pause_game_button(self))
        pause_button.set_size((button_length, button_height))

        reset_button = thorpy.make_button("Reset", func=lambda: gui_controls.reset_game_button(self))
        reset_button.set_size((button_length, button_height))

        undo_button = thorpy.make_button("Undo", func=lambda: gui_controls.undo_move_button(self))
        undo_button.set_size((button_length, button_height))

        controls_box = thorpy.Box.make(elements=[
            starting_position_title, starting_position_dropdown,
            start_button, stop_button, pause_button, reset_button, undo_button
        ])
        controls_box.set_size((225, 450))

        ### PLAYER SETTINGS ###
        black_settings_title = thorpy.make_text("Black", 22, (0,0,0))
        black_settings_title.set_size((button_length, button_height))

        black_move_limit = thorpy.Inserter("Move Limit:", value="")
        black_move_limit.set_size((button_length/2, button_height/2))

        black_time_limit = thorpy.Inserter(name="Time Limit", value="")
        black_time_limit.set_size((button_length/2, button_height/2))

        # Black human or AI radio group
        black_human_radio = thorpy.Checker.make("Human", type_="radio")
        black_ai_radio = thorpy.Checker.make("AI", type_="radio")
        black_radio_choices = [black_human_radio, black_ai_radio]
        black_radio_group = thorpy.RadioPool(black_radio_choices,
                                             first_value=black_radio_choices[0],
                                             always_value=True)

        # White human or AI radio group
        white_human_radio = thorpy.Checker.make("Human", type_="radio")
        white_ai_radio = thorpy.Checker.make("AI", type_="radio")
        white_radio_choices = [white_human_radio, white_ai_radio]
        white_radio_group = thorpy.RadioPool(white_radio_choices,
                                             first_value=white_radio_choices[0],
                                             always_value=True)

        white_settings_title = thorpy.make_text("White", 22, (0, 0, 0))
        white_settings_title.set_size((button_length, button_height))

        white_move_limit = thorpy.Inserter(name="Move Limit", value="")
        white_move_limit.set_size((button_length/2, button_height/2))

        white_time_limit = thorpy.Inserter("Time Limit", value="")
        white_time_limit.set_size((button_length/2, button_height/2))

        # Put this in a list for sanitization later
        self.settings_inputs = [black_move_limit, black_time_limit, white_move_limit, white_time_limit]

        settings_box = thorpy.Box.make(elements=[
            black_settings_title, black_human_radio, black_ai_radio, black_move_limit, black_time_limit,
            white_settings_title, white_human_radio, white_ai_radio, white_move_limit, white_time_limit,
        ])
        settings_box.set_size((225, 450))

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
        move_box.set_size((225, 450))


        # Set the position of each box, then place
        controls_box.set_topleft((console_start_x, console_start_y))
        controls_box.blit()
        controls_box.update()

        settings_box.set_topleft((console_start_x + 225, 0))
        settings_box.blit()
        settings_box.update()

        move_box.set_topleft((console_start_x, 450))
        move_box.blit()
        move_box.update()

        self.console = thorpy.Menu([controls_box, settings_box, move_box])
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
                # TODO: The following two lines should be called in game_state
                # self.board.update_board(self.window)
                # self.toggle_player_move()   # Other players turn.
                self.end_turn()

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

    def end_turn(self):
        # self.toggle_player_move()
        game_state.update_turn(self)

    def toggle_player_move(self):
        if self.player_turn == Turn.WHITE:
            self.player_turn = Turn.BLACK
        else:
            self.player_turn = Turn.WHITE
        print(f"{self.player_turn.name} to move!")

    def draw_score_and_time(self):
        """
        Builds the boxes for black and white score, time taken, and moves taken.
        Should only be called on startup and resetting the board
        """
        ##### BLACK #####
        black_score_title = thorpy.make_text("Black", 24, (0,0,0))
        black_score_title.set_topleft((50, 640))
        black_score_title.blit()
        black_score_title.update()

        font_text_time_label = pygame.font.SysFont('Ariel', 30)
        black_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(black_total_time_taken, (25, 675))

        black_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(black_turn_time_taken, (25, 705))

        black_score = font_text_time_label.render("Score:", True, black)
        self.window.blit(black_score, (25, 735))

        black_moves_taken = font_text_time_label.render("Moves Taken:", True, black)
        self.window.blit(black_moves_taken, (25, 765))


        ##### WHITE #####
        white_score_title = thorpy.make_text("White:", 24, (0,0,0))
        white_score_title.set_topleft((550, 640))
        white_score_title.blit()

        white_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(white_total_time_taken, (525, 675))

        white_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(white_turn_time_taken, (525, 705))

        white_score = font_text_time_label.render("Score:", True, black)
        self.window.blit(white_score, (525, 735))

        white_moves_taken = font_text_time_label.render("Moves Taken:", True, black)
        self.window.blit(white_moves_taken, (525, 765))

        current_turn = font_text_time_label.render("Current Turn:", True, black)
        self.window.blit(current_turn, (590, 25))

        pygame.display.update()

    def set_scoreboard(self):
        # For setting or resetting the score, time, etc.
        self.draw_score_and_time()
        self.update_total_time(Turn.BLACK, "0")
        self.update_total_time(Turn.WHITE, "0")
        self.update_turn_time(Turn.BLACK, "0")
        self.update_turn_time(Turn.WHITE, "0")
        self.update_score(Turn.BLACK, "0")
        self.update_score(Turn.WHITE, "0")
        self.update_moves_taken(Turn.BLACK, "0")
        self.update_moves_taken(Turn.WHITE, "0")
        self.update_turn_label(Turn.BLACK)


    def update_total_time(self, piece_enum, time):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            time_taken = font_text_time_label.render(time, True, black)
            self.window.blit(time_taken, white_total_time_location)
        elif piece_enum == Turn.BLACK:
            time_taken = font_text_time_label.render(time, True, black)
            self.window.blit(time_taken, black_total_time_location)

    def update_turn_time(self, piece_enum, time):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            time_taken = font_text_time_label.render(time, True, black)
            self.window.blit(time_taken, white_turn_time_taken_location)
        elif piece_enum == Turn.BLACK:
            time_taken = font_text_time_label.render(time, True, black)
            self.window.blit(time_taken, black_turn_time_location)

    def update_score(self, piece_enum, score):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            time_taken = font_text_time_label.render(score, True, black)
            self.window.blit(time_taken, white_score_location)
        elif piece_enum == Turn.BLACK:
            time_taken = font_text_time_label.render(score, True, black)
            self.window.blit(time_taken, black_score_location)

    def update_moves_taken(self, piece_enum, moves_taken):
        font_text_time_label = pygame.font.SysFont('Ariel', 30)

        if piece_enum == Turn.WHITE:
            time_taken = font_text_time_label.render(moves_taken, True, black)
            self.window.blit(time_taken, white_moves_taken_location)
        elif piece_enum == Turn.BLACK:
            time_taken = font_text_time_label.render(moves_taken, True, black)
            self.window.blit(time_taken, black_moves_taken_location)

    def update_turn_label(self, piece_enum):
        font_text_time_lable = pygame.font.SysFont('Ariel', 30)
        turn_label = font_text_time_lable.render(piece_enum.name, True, black)
        self.window.blit(turn_label, turn_label_location)
