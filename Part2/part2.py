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
tile = next(this_turn)


def repeating_tasks(r, c, change_row, change_column):
    coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    move_notation = "{coor}/{row_notation}{column_notation}".format(
        coor=coor, row_notation=MOVE_NOTATION_MAP[change_row], column_notation=MOVE_NOTATION_MAP[change_column])
    r += change_row
    c += change_column
    new_coor = "{row}{column}".format(row=RowMapper(r).name, column=c + 1)
    temp_tiles.append((Tile(r, c, new_coor, current_turn), move_notation))


# Minus minus
repeating_tasks(tile.row, tile.column, -1, -1)
# Minus zero
repeating_tasks(tile.row, tile.column, -1, 0)
# Zero minus
repeating_tasks(tile.row, tile.column, 0, -1)
# Zero plus
repeating_tasks(tile.row, tile.column, 0, 1)
# Plus zero
repeating_tasks(tile.row, tile.column, 1, 0)
# Plus plus
repeating_tasks(tile.row, tile.column, 1, 1)

for tile_tuple in temp_tiles:
    tile = tile_tuple[0]
    if 0 <= tile.row <= 8\
            and tile.column in BOARD_LIMITS[tile.row]\
            and tile not in tile_layout:
        new_layouts.append(tile)
        moves.append(tile_tuple[1])

for tile in new_layouts:
    print(tile)

for move in moves:
    print(move)



# Filter only the black/white pieces, depending on whose turn it is.
this_turn = (piece for piece in current_layout[1] if current_layout[0] in piece)

