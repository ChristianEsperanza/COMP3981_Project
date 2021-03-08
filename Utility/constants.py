import pygame
"""
Constants to be used throughout the program.
"""

# Colors
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]


# Dimensions
window_width = 1300
window_height = 900

piece_radius = 25
piece_distance = 20

board_width = window_width - 550
board_height = window_height
board_start_x = 20
board_start_y = 30

# Console starts where board ends
console_width = window_width - board_width
console_height = window_height
# console_start_x = window_width - console_width + 10
console_start_x = board_width + 10
console_start_y = 0

# Misc
num_rows = 9
max_row = 9