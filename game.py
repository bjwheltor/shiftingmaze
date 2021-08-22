"""
Main game control code

History
24-Jul-2021 - Initial version
21-Aug-2021 - Simplified control
"""
import sys
import pygame
import numpy as np

from position import *
from tiles import *
from player import *
from board import *
from plot import *

pygame.init()

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

# Create a tile set and fill tile bag
test_tileset = False

if test_tileset:
    tileset_name = "test"
    doors_for_tiles = {
        0: [1, 1, 1, 1],
    }
    tile_counts = {0: 300}
else:
    tileset_name = "standard"
    doors_for_tiles = {
        0: [1, 1, 1, 1],
        1: [0, 1, 1, 1],
        2: [0, 0, 1, 1],
        3: [0, 1, 0, 1],
        4: [0, 0, 0, 1],
    }
    tile_counts = {0: 40, 1: 140, 2: 80, 3: 80, 4: 20}

tile_set = TileSet(doors_for_tiles, tile_counts, name=tileset_name)
tile_bag = TileBag(tile_set)
tile_size = tile_set.tiles[0].size

# Set (full) board and (board) view dimensions in tiles using Position
# board and view dimensions must be an odd numbers
board_xy = Position(15, 15)
view_xy = Position(9, 9)
player_xy = Position(board_xy.x // 2, board_xy.y // 2)
shift_xy = Position((board_xy.x - view_xy.x) // 2, (board_xy.y - view_xy.y) // 2)


# Create board and fill with tiles from tile bag
board = Board(board_xy, tile_bag=tile_bag)

# create player
player_name = "Bruce"
player_number = 1
player_colour = GREEN
player = Player(player_name, player_number, player_colour, player_xy)

# create display
plot = Plot(
    view_xy.x,
    view_xy.y,
    board_xy.x,
    board_xy.y,
    tile_size,
    position_shift=shift_xy,
)
plot.show_all_tiles(board.placements, board.orientations, tile_set.tiles)

# draw player
plot.show_player(player)
print(f"Player postion: {player.position}")

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

                next_position = player.position.get_next(direction)

                # trying to move off edge of board
                if (
                    next_position.x < 0
                    or next_position.y < 0
                    or next_position.x >= total_x_tiles
                    or next_position.y >= total_y_tiles
                ):
                    pass
                # no door in current room in direction of intended movement
                elif not board.check_for_door(
                    player.position, direction, tile_set.tiles
                ):
                    pass
                # no door in next roon in direction of intended movement
                elif not board.check_for_door(
                    player.position, direction, tile_set.tiles, next=True
                ):
                    pass
                # movement is possible
                else:
                    plot.move_player(
                        player,
                        direction,
                        board.tile_placements,
                        board.tile_orientations,
                        tile_set.tiles,
                    )
                    player.position.move(direction)
                print(
                    f"Player postion: {player.position}    Position shift: {position_shift}"
                )

            elif event.key in ROTATE_KEYS:
                if event.key == pygame.K_z:
                    rotation = 1
                elif event.key == pygame.K_x:
                    rotation = -1
                plot.rotate_tile(player.position, rotation)
                board.rotate_tile(player.position, rotation)
