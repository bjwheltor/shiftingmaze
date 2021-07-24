"""
Main game control code

History
24-Jul-2021 - Initial version
"""
import os
import sys
import random
import pygame
import numpy as np

from position import *
from tiles import *
from player import *
from board import *
from plot import *

# Define colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (192, 192, 192)
BLACK = (0, 0, 0)
BLUE = (150, 150, 255)
YELLOW = (200, 200, 0)
RED = (200, 100, 100)
GREEN = (100, 200, 100)

MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
ROTATE_KEYS = (pygame.K_z, pygame.K_x)
SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)

# Create a tileset
doors_for_tiles = {
    0: [1, 1, 1, 1],
    1: [0, 1, 1, 1],
    2: [0, 0, 1, 1],
    3: [0, 1, 0, 1],
    4: [0, 0, 0, 1],
}
tile_counts = {0: 40, 1: 140, 2: 80, 3: 80, 4: 20}
tile_set = TileSet(doors_for_tiles, tile_counts, name="standard")
tile_bag = TileBag(tile_set)

# Create board and fill with tiles from tile bag
board_width = 15
board_height = 15
board = Board(width=board_width, height=board_height, tile_bag=tile_bag)

x_tile_range = list(range(board_width))
y_tile_range = list(range(board_height))
rotation_range = list(range(-1, 2, 2))

# create player
player_name = "Bruce"
player_number = 1
player_colour = GREEN
player_position = Position(int(board_width / 2), int(board_height / 2))
player = Player(player_name, player_number, player_colour, player_position)

# create board display
x_tiles = 9
y_tiles = 9
tile_size = tile_set.tiles[0].size

position_shift = Position(
    int((board_width - x_tiles) / 2), int((board_height - y_tiles) / 2)
)

plot = Plot(x_tiles, y_tiles, tile_size)
plot.show_all_tiles(
    board.tile_placements,
    board.tile_orientations,
    tile_set.tiles,
    position_shift=position_shift,
)

# draw player
plot.show_player(player, position_shift=position_shift)

# gaming loop
while True:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key in MOVE_KEYS:
                if event.key == pygame.K_UP:
                    direction = Position.UP
                elif event.key == pygame.K_LEFT:
                    direction = Position.LEFT
                elif event.key == pygame.K_DOWN:
                    direction = Position.DOWN
                elif event.key == pygame.K_RIGHT:
                    direction = Position.RIGHT
                player.position.move(direction)

                new_x, new_y = new_xy_from_direction(player.x, player.y, direction)
                current_clear, new_clear = board.access_in_direction(
                    player.x, player.y, direction
                )
                plot.move_player(
                    player.image,
                    player.x,
                    player.y,
                    new_x,
                    new_y,
                    current_clear,
                    new_clear,
                )
                if new_clear:
                    player.move(new_x, new_y)
            elif event.key in ROTATE_KEYS:
                if event.key == pygame.K_z:
                    rotation = 1
                elif event.key == pygame.K_x:
                    rotation = -1
                tile_x = player.x
                tile_y = player.y
                tile_number = board.tile_placements[tile_x, tile_y]
                tile_image = tiles[tile_number].image
                plot.rotate_tile(tile_image, player.image, tile_x, tile_y, rotation)
                board.rotate_tile(tile_x, tile_y, rotation)
            elif event.key in SLIDE_ROW_KEYS:
                if event.key == pygame.K_q:
                    slide = 1
                elif event.key == pygame.K_w:
                    slide = -1
                row_y = 5
                plot.slide_row(row_y, slide)
                board.slide_row(row_y, slide)
            elif event.key in SLIDE_COLUMN_KEYS:
                if event.key == pygame.K_p:
                    slide = 1
                elif event.key == pygame.K_l:
                    slide = -1
                column_x = 5
                plot.slide_column(column_x, slide)
                board.slide_column(column_x, slide)
