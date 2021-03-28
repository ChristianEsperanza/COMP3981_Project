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
        self.alternate_turns = True
        self.toggle_players = True
        self.board = Board()
        self.window = None
        self.console = None
        self.selected_pieces = []
        self.player_turn = Turn.WHITE

    def run(self):
        """
        Builds the GUI and then runs the main loop, calling methods to build different pieces
        """
        # Build window, board, console
        self.build_window()
        self.board.build_board(self.window)
        self.build_console()
        event = None

        print(f"{self.player_turn.name} to move!")

        # TODO: Rename this function
        self.draw_score_and_time()

        pygame.display.set_caption("Abalone")
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    print(pos)
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
        :return:
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
        # starting_position_dropdown = thorpy.DropDownList(titles=starting_positions)
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

        black_move_limit = thorpy.make_button("Move Limit", func=self.test_func)
        black_move_limit.set_size((button_length, button_height))

        black_time_limit = thorpy.make_button("Time Limit", func=self.test_func)
        black_time_limit.set_size((button_length, button_height))

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

        white_settings_title = thorpy.make_text("White", 22, (0,0,0))
        white_settings_title.set_size((button_length, button_height))

        white_move_limit = thorpy.make_button("Move Limit", func=self.test_func)
        white_move_limit.set_size((button_length, button_height))

        white_time_limit = thorpy.make_button("Time Limit", func=self.test_func)
        white_time_limit.set_size((button_length, button_height))

        white_human_computer_choice = thorpy.make_button("Human or AI", func=self.test_func)
        white_human_computer_choice.set_size((button_length, button_height))

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
        # # print(f"{self.player_turn.name} to move!")
        # print("Move: " + str(kwargs['vector']))
        # vector_rep = kwargs['vector']
        #
        # try:
        #
        #     vector = None
        #     selected_pieces_sorted = None
        #
        #     # Moving of pieces. Sorting used for correct movement of pieces.
        #     if vector_rep == Vector.UP_LEFT:
        #         vector = (1, 0)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'), reverse=True)
        #     elif vector_rep == Vector.UP_RIGHT:
        #         vector = (1, 1)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'), reverse=True)
        #     elif vector_rep == Vector.LEFT:
        #         vector = (0, -1)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'))
        #     elif vector_rep == Vector.RIGHT:
        #         vector = (0, 1)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'), reverse=True)
        #     elif vector_rep == Vector.DOWN_LEFT:
        #         vector = (-1, -1)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'))
        #     elif vector_rep == Vector.DOWN_RIGHT:
        #         vector = (-1, 0)
        #         selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('row', 'column'))
        #
        #     if self.is_valid_selection() and self.is_valid_move(vector_rep):
        #
        #         # Swaps all tiles according to movement vector
        #         for tile in selected_pieces_sorted:
        #             print(f"Moving vector {vector}")
        #             self.board.swap_tiles((tile.row, tile.column), (tile.row + vector[0], tile.column + vector[1]))
        #         self.board.update_board(self.window)
        #
        #         self.toggle_player_move()   # Other players turn.
        #
        #     else:
        #         print("Invalid Move. Clearing selected pieces")
        #
        # except KeyError:
        #     print("Middle Button pressed")
        #
        # finally:
        #     self.selected_pieces.clear()
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

            if len(selected_pieces_sorted) == 0:
                print("No pieces to move")
                return

            if self.is_valid_selection() and self.is_valid_move(vector, selected_pieces_sorted):

                target_coord = self.find_target_coord(vector, selected_pieces_sorted)

                # # Evaluate push on opponent piece.
                # if self.board.board_dict[target_coord].piece != (self.player_turn.value or None):
                #     print(f"Evaluated Push Strength: {self.find_opposing_push_strength(target_coord, vector)}")

                # Swaps all tiles according to movement vector
                for tile in selected_pieces_sorted:
                    print(f"Moving vector {vector}")
                    self.board.swap_tiles((tile.row, tile.column), (tile.row + vector[0], tile.column + vector[1]))
                self.board.update_board(self.window)

                if self.toggle_players:
                    self.toggle_player_move()  # Other players turn.

                return True
            else:
                print("Invalid Move. Clearing selected pieces")
                return False

        # except KeyError:
        #     print("Middle Button pressed")

        finally:
            self.selected_pieces.clear()

    def is_valid_selection(self):
        # print("POG")
        # if len(self.selected_pieces) > 3:
        #     return False
        # prev_tile = None
        # selected_pieces_sorted = sorted(self.selected_pieces, key=itemgetter('column'))
        # for tile in selected_pieces_sorted:
        #     print(tile)
        #     if tile.piece != self.player_turn.value:
        #         print("Wrong color")
        #         return False
        #     if prev_tile is not None:
        #         if prev_tile.row != tile.row or prev_tile.column != tile.column - 1:
        #             print(f"{prev_tile.column}, {tile.column}")
        #             print("Inconsistent row selection")
        #             return False
        #         else:
        #             prev_tile = tile
        #     else:
        #         prev_tile = tile
        # return True
        print("Evaluating for valid selection")
        if len(self.selected_pieces) > 3:
            return False
        # prev_tile = None
        selected_pieces_sorted_col = sorted(self.selected_pieces, key=itemgetter('column'))
        for tile in selected_pieces_sorted_col:
            print(tile)
            # Determine consistent piece selection
            if self.alternate_turns and tile.piece != self.player_turn.value:
                print("Wrong color")
                return False

        if not self.is_continuous_row_selection() and not self.is_continuous_diagonal_selection():
            print("Non continuous selection")
            return False
        print("Invalid Selection")
        return True

    def is_continuous_row_selection(self):
        prev_tile = None
        selected_pieces_sorted_col = sorted(self.selected_pieces, key=itemgetter('column'))

        # Determine continuous row selection
        for tile in selected_pieces_sorted_col:
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

    def is_continuous_diagonal_selection(self):
        # print("Starting Diagonal selection consistency Test.")
        prev_tile = None
        selected_pieces_sorted_row = sorted(self.selected_pieces, key=itemgetter('row'))
        horizontal_vector = None  # Keeps track on either up-right or up-left consistency

        # Determine Continuous diagonal selection
        for tile in selected_pieces_sorted_row:

            # Determine continuous row selection
            if prev_tile is not None:
                if horizontal_vector is None:
                    # Assign horizontal vector based on first and second evaluation.
                    if prev_tile.column + 1 == tile.column:
                        horizontal_vector = 1
                        # print("Looking for up-right diagonal")
                    else:
                        horizontal_vector = 0
                        # print("Looking for up-left diagonal")
                if prev_tile.row + 1 == tile.row:  # Row consistency (increasing)
                    # print(f"Evaluating tile: {prev_tile.column}, {tile.column}")
                    if horizontal_vector is not None:
                        if prev_tile.column + horizontal_vector != tile.column:
                            # print(f"Inconsistent column selection: c1:{prev_tile.column} c2:{tile.column}")
                            return False
                    else:
                        print("Horizontal_vector wasn't assigned. Something went wrong")
                else:
                    # print("Inconsistent row selection")
                    return False
                prev_tile = tile
            else:
                # After first evaluation, assign some variables
                prev_tile = tile
        return True

    def is_valid_move(self, vector: tuple, selected_pieces_sorted: list):
        # board_seq = ('I5', 'I6', 'I7', 'I8', 'I9', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'G3', 'G4', 'G5', 'G6', 'G7',
        #              'G8', 'G9', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
        #              'E7', 'E8', 'E9', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'C1', 'C2', 'C3', 'C4', 'C5',
        #              'C6', 'C7', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'A1', 'A2', 'A3', 'A4', 'A5')
        # for tile in self.selected_pieces:
        #     if tile.board_coordinate not in board_seq:
        #         print("Can't move out of bounds.")
        #         return False
        # return True
        print("Evaluating if move is valid")
        try:
            target_coord = self.find_target_coord(vector, selected_pieces_sorted)
            print("Target Coord:", end="")
            print(target_coord)
        except KeyError:
            print("Can't move out of bounds.")
            return False

        # Friendly collisions
        print("------Starting Friendly Piece Collision-----")
        if self.determine_piece_collision(vector, selected_pieces_sorted, self.player_turn):
            print("Cannot push your own piece.")
            return False

        if self.player_turn == Turn.BLACK:
            opponent_piece = Turn.WHITE
        else:
            opponent_piece = Turn.BLACK

        # Opponent piece collisions
        # do_stuff = True
        print("------Starting Opponent Piece Collision-----")
        if self.determine_piece_collision(vector, selected_pieces_sorted, opponent_piece):
            print("Collision with opponent piece. Do stuff")
            print("\nDetermining Push")
            if self.is_linear_movement(vector, selected_pieces_sorted):
                print(f"Target Coord: {target_coord}")
                opponent_push_strength = self.find_opposing_push_strength(target_coord, vector)
                print(f"Opp push strength: "
                      f"{opponent_push_strength}")
                if (len(self.selected_pieces) > opponent_push_strength) and (opponent_push_strength != 0):
                    print("SUMITO!!!!!")
                    self.sumito(vector, target_coord)
                    return True
                else:
                    print("Failed Push!")
                    return False
            else:
                print("Collision with non-linear movement. Invalid Move")
                print("Result Vector:")
                print(vector)
                print("Coord")
                for tile in selected_pieces_sorted:
                    print(tile.board_coordinate)
                return False
        return True

    def is_linear_movement(self, vector: tuple, selected_pieces_sorted: list):
        print("Linear move test")
        if len(selected_pieces_sorted) == 1:
            return True
        if self.change_coordinate_by_vector(vector, selected_pieces_sorted[1]) == selected_pieces_sorted[0].board_coordinate:
            return True
        else:
            return False

    def sumito(self, vector, target_coord):
        current_tile = self.board.board_dict[target_coord]
        temp_prev = None
        # temp_curr = None
        try:
            while current_tile.piece is not None:
                temp_curr = current_tile.piece
                print(current_tile)
                self.board.board_dict[current_tile.board_coordinate].piece = temp_prev
                temp_prev = temp_curr
                current_tile = self.board.board_dict[self.change_coordinate_by_vector(vector, current_tile)]

            current_tile.piece = temp_prev
            return
        except KeyError:
            return

    def determine_piece_collision(self, vector: tuple, selected_pieces_sorted: list, collision_piece_id):
        for tile in selected_pieces_sorted:
            evaluated_next_coord = self.change_coordinate_by_vector(vector, tile)
            evaluated_next_tile = self.board.board_dict[evaluated_next_coord]
            print(f"Current:{tile.board_coordinate}-----Evaluated:{evaluated_next_coord}")
            if evaluated_next_tile.piece == collision_piece_id.value \
                    and evaluated_next_tile not in selected_pieces_sorted:
                print(f"Collision with {collision_piece_id.name}")
                return True
        return False

    @staticmethod
    def change_coordinate_by_vector(vector: tuple, tile):
        new_coord = f"{chr(ord(tile.board_coordinate[0]) + vector[0])}{int(tile.board_coordinate[1]) + vector[1]}"
        return new_coord

    def find_target_coord(self, vector, selected_pieces_sorted):
        coord = self.change_coordinate_by_vector(vector, selected_pieces_sorted[0])
        print("Target coord: ", end="")
        print(coord)
        return self.board.board_dict[coord].board_coordinate

    def find_opposing_push_strength(self, contact_tile, vector):

        push_strength = 0
        try:
            current_tile = self.board.board_dict[contact_tile]
            while True:
                print(f"Current Eval Coord: " + current_tile.board_coordinate + "----Piece: " + str(current_tile.piece))
                if current_tile.piece is None:
                    print("Out by None")
                    return push_strength
                else:
                    next_coord = self.change_coordinate_by_vector(vector, current_tile)
                    print(f"Next coord: {next_coord}")
                    push_strength += 1
                    current_tile = self.board.board_dict[next_coord]
                    print("Incrementing push strength")
                    print(f"Eval Coord: " + current_tile.board_coordinate + "----Piece: " + str(current_tile.piece))
        except KeyError:
            return push_strength

    def toggle_player_move(self):
        if self.player_turn == Turn.WHITE:
            self.player_turn = Turn.BLACK
        else:
            self.player_turn = Turn.WHITE
        print(f"{self.player_turn.name} to move!")

    def draw_score_and_time(self):
        """
        Builds the boxes for black and white score, time taken,
        and moves taken
        """
        #TODO: Draw a box behind these
        black_score_title = thorpy.make_text("Black", 22, (0,0,0))
        black_score_title.set_topleft((50, 640))
        black_score_title.blit()

        font_text_time_label = pygame.font.SysFont('Ariel', 30)
        black_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(black_total_time_taken, (25, 675))

        black_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(black_turn_time_taken, (25, 705))

        white_score_title = thorpy.make_text("White:", 22, (0,0,0))
        white_score_title.set_topleft((570, 640))
        white_score_title.blit()

        white_total_time_taken = font_text_time_label.render("Total Time:", True, black)
        self.window.blit(white_total_time_taken, (545, 675))

        white_turn_time_taken = font_text_time_label.render("Turn Time:", True, black)
        self.window.blit(white_turn_time_taken, (545, 705))

    def update_score_and_time(self):
        pass
