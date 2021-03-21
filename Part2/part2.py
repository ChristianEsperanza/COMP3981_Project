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

moves = []
new_layouts = []
temp_tiles = []


def move_piece(r, c, change_row, change_column):
    coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    move_notation = "{coor}/{row_notation}{column_notation}".format(
        coor=coor, row_notation=MOVE_NOTATION_MAP[change_row], column_notation=MOVE_NOTATION_MAP[change_column])
    r += change_row
    c += change_column
    new_coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    temp_tiles.append((Tile(r, c, new_coor, current_turn), move_notation))


for tile in this_turn:
    # Minus minus
    move_piece(tile.row, tile.column, -1, -1)
    # Minus zero
    move_piece(tile.row, tile.column, -1, 0)
    # Zero minus
    move_piece(tile.row, tile.column, 0, -1)
    # Zero plus
    move_piece(tile.row, tile.column, 0, 1)
    # Plus zero
    move_piece(tile.row, tile.column, 1, 0)
    # Plus plus
    move_piece(tile.row, tile.column, 1, 1)

    for tile_tuple in temp_tiles:
        layout_for_this_move = tile_layout.copy()
        new_tile = tile_tuple[0]
        if 0 <= new_tile.row <= 8 \
                and new_tile.column in BOARD_LIMITS[new_tile.row] \
                and new_tile not in layout_for_this_move:
            layout_for_this_move.remove(tile)
            layout_for_this_move.append(new_tile)
            layout_for_this_move.sort()
            new_layouts.append(layout_for_this_move)
            moves.append(tile_tuple[1])
    temp_tiles.clear()

for layout in new_layouts:
    for tile in layout:
        print(tile, end=",")
    print()

for move in moves:
    print(move)
