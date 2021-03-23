import enum

from GUI.tile import Tile
from file_reader import FileReader


class RowMapper(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8


BOARD_LIMITS = {
    0: {0, 1, 2, 3, 4},
    1: {0, 1, 2, 3, 4, 5},
    2: {0, 1, 2, 3, 4, 5, 6},
    3: {0, 1, 2, 3, 4, 5, 6, 7},
    4: {0, 1, 2, 3, 4, 5, 6, 7, 8},
    5: {1, 2, 3, 4, 5, 6, 7, 8},
    6: {2, 3, 4, 5, 6, 7, 8},
    7: {3, 4, 5, 6, 7, 8},
    8: {4, 5, 6, 7, 8}
}

MOVE_NOTATION_MAP = {
    -1: "-",
    0: "0",
    1: "+"
}

data = FileReader.load_data("Test1.input")
current_layout = FileReader.read_data(data)
current_turn_letter = current_layout[0]
tile_layout = []
current_turn = 1 if current_layout[0] == "w" else 2
for piece in current_layout[1]:
    row = RowMapper[piece[0]].value
    column = int(piece[1]) - 1
    piece_color = 1 if piece[2] == "w" else 2
    coordinates = piece[:-1]
    tile_layout.append(Tile(row, column, coordinates, piece_color))

this_turn = (tile for tile in tile_layout if tile.piece == current_turn)
my_coordinates = [tile.board_coordinate for tile in tile_layout if tile.piece == current_turn]
opponent_coordinates = [tile.board_coordinate for tile in tile_layout if tile.piece != current_turn]

moves = []
new_layouts = []
unvalidated_moves = []
doubles = []
triples = []


def move_single_piece(tile, change_row, change_column):
    coor = "{row}{column}".format(row=RowMapper(tile.row).name, column=tile.column + 1)
    move_note = "{coor}/{row_notation}{column_notation}".format(
        coor=coor, row_notation=MOVE_NOTATION_MAP[change_row], column_notation=MOVE_NOTATION_MAP[change_column])
    r = tile.row + change_row
    c = tile.column + change_column
    new_coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    unvalidated_moves.append((Tile(r, c, new_coor, current_turn), move_note))


def move_two_pieces(tile_double, change_row, change_column):
    tile1 = tile_double[0]
    tile2 = tile_double[1]
    coor = "{row1}{column1}:{row2}{column2}".format(row1=RowMapper(tile1.row).name, column1=tile1.column + 1,
                                                    row2=RowMapper(tile2.row).name, column2=tile2.column + 1)
    move_notation = "{coor}/{row_notation}{column_notation}".format(
        coor=coor, row_notation=MOVE_NOTATION_MAP[change_row], column_notation=MOVE_NOTATION_MAP[change_column])
    r1 = tile1.row + change_row
    c1 = tile1.column + change_column
    r2 = tile2.row + change_row
    c2 = tile2.column + change_column
    sumito = True if abs(tile2.row - tile1.row) == abs(change_row)\
        and abs(tile2.column - tile1.column) == abs(change_column) else False
    coor1 = "{row}{column}".format(row=RowMapper(r1).name, column=c1 + 1)
    coor2 = "{row}{column}".format(row=RowMapper(r2).name, column=c2 + 1)
    new_tile1 = Tile(r1, c1, coor1, current_turn)
    new_tile2 = Tile(r2, c2, coor2, current_turn)
    new_pair = (new_tile1, new_tile2)
    tile_1_is_leader = True if change_row + change_column < 0 else False
    unvalidated_moves.append((new_pair, sumito, move_notation, tile_1_is_leader, change_row, change_column))


def find_doubles(tile):
    # Zero plus
    r = tile.row
    c = tile.column + 1
    coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    zp = Tile(r, c, coor, current_turn)
    # Plus zero
    r = tile.row + 1
    c = tile.column
    coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    pz = Tile(r, c, coor, current_turn)
    # Plus plus
    r = tile.row + 1
    c = tile.column + 1
    coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    pp = Tile(r, c, coor, current_turn)

    if zp in tile_layout:
        doubles.append((tile, zp))
    if pz in tile_layout:
        doubles.append((tile, pz))
    if pp in tile_layout:
        doubles.append((tile, pp))


def find_triples():
    for pair in doubles:
        first_piece = pair[0]
        second_piece = pair[1]
        r = 2 * second_piece.row - first_piece.row
        c = 2 * second_piece.column - first_piece.column
        coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
        third_piece = Tile(r, c, coor, current_turn)
        if third_piece in tile_layout:
            triples.append((first_piece, second_piece, third_piece))


def move_all_single_pieces():
    for tile in this_turn:
        find_doubles(tile)
        # Minus minus
        move_single_piece(tile, -1, -1)
        # Minus zero
        move_single_piece(tile, -1, 0)
        # Zero minus
        move_single_piece(tile, 0, -1)
        # Zero plus
        move_single_piece(tile, 0, 1)
        # Plus zero
        move_single_piece(tile, 1, 0)
        # Plus plus
        move_single_piece(tile, 1, 1)

        for tile_tuple in unvalidated_moves:
            layout_for_this_move = tile_layout.copy()
            new_tile = tile_tuple[0]
            if 0 <= new_tile.row <= 8 \
                    and new_tile.column in BOARD_LIMITS[new_tile.row] \
                    and new_tile.board_coordinate not in my_coordinates \
                    and new_tile.board_coordinate not in opponent_coordinates:
                layout_for_this_move.remove(tile)
                layout_for_this_move.append(new_tile)
                layout_for_this_move.sort()
                new_layouts.append(layout_for_this_move)
                moves.append(tile_tuple[1])
        unvalidated_moves.clear()


def move_all_double_pieces():
    for double in doubles:
        move_two_pieces(double, -1, -1)
        move_two_pieces(double, -1, 0)
        move_two_pieces(double, 0, -1)
        move_two_pieces(double, 0, 1)
        move_two_pieces(double, 1, 0)
        move_two_pieces(double, 1, 1)

        for pair_tuple in unvalidated_moves:
            layout_for_this_move = tile_layout.copy()
            new_pair = pair_tuple[0]
            sumito = pair_tuple[1]
            move_notation = pair_tuple[2]
            tile1 = new_pair[0]
            tile2 = new_pair[1]
            # Board limits
            tile1_bounded = True if 0 <= tile1.row <= 8 and tile1.column in BOARD_LIMITS[tile1.row] else False
            tile2_bounded = True if 0 <= tile2.row <= 8 and tile2.column in BOARD_LIMITS[tile2.row] else False
            if not (tile1_bounded and tile2_bounded):
                continue
            if not sumito:
                # Own pieces in the way
                tile1_open = True if tile1.board_coordinate not in my_coordinates else False
                tile2_open = True if tile2.board_coordinate not in my_coordinates else False
                if not (tile1_open and tile2_open):
                    continue
                # Enemy pieces are in the way
                tile1_free = True if tile1.board_coordinate not in opponent_coordinates else False
                tile2_free = True if tile2.board_coordinate not in opponent_coordinates else False
                if not (tile1_free and tile2_free):
                    continue
            else:
                tile_1_is_leader = pair_tuple[3]
                change_row = pair_tuple[4]
                change_column = pair_tuple[5]
                lead_tile = tile1 if tile_1_is_leader else tile2
                # Own pieces in the way
                if lead_tile.board_coordinate in my_coordinates:
                    continue
                if lead_tile.board_coordinate in opponent_coordinates:
                    next_enemy_row = lead_tile.row + change_row
                    next_enemy_column = lead_tile.column + change_column
                    enemy_coor = "{row}{column}".format(row=RowMapper(next_enemy_row).name,
                                                        column=next_enemy_column + 1)
                    if enemy_coor in opponent_coordinates:
                        continue
                    if enemy_coor in my_coordinates:
                        continue
                    enemy_color = 2 if lead_tile.piece == 1 else 1
                    enemy_previous_position = Tile(lead_tile.row, lead_tile.column,
                                                   lead_tile.board_coordinate, enemy_color)
                    enemy_next_position = Tile(next_enemy_row, next_enemy_column, enemy_coor, enemy_color)
                    layout_for_this_move.remove(enemy_previous_position)
                    if 0 <= enemy_next_position.row <= 8 \
                            and enemy_next_position.column in BOARD_LIMITS[enemy_next_position.row]:
                        layout_for_this_move.append(enemy_next_position)
            layout_for_this_move.remove(double[0])
            layout_for_this_move.remove(double[1])
            layout_for_this_move.append(tile1)
            layout_for_this_move.append(tile2)
            layout_for_this_move.sort()
            new_layouts.append(layout_for_this_move)
            moves.append(move_notation)
        unvalidated_moves.clear()


move_all_single_pieces()
find_triples()
move_all_double_pieces()

num = 1
with open("test.board", mode="w", encoding="utf-8") as board_file:
    for layout in new_layouts:
        for tile in layout:
            board_file.write(tile.__str__())
            board_file.write(",")
        board_file.write("\n")

with open("test.move", mode="w", encoding="utf-8") as move_file:
    for move in moves:
        move_file.write(f"{move}\n")

# for two_pieces in doubles:
#     print(f"({two_pieces[0]}, {two_pieces[1]})")

for triple in triples:
    print(f"({triple[0]}, {triple[1]}, {triple[2]})")
