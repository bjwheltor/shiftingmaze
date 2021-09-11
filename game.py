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
from text import *

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

# Set up event information
MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
ROTATE_KEYS = (pygame.K_z, pygame.K_x)
SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)
RANDOM = pygame.USEREVENT + 0

pygame.time.set_timer(RANDOM, 3000)

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

# Set (full) board dimensions in tiles using Position - must be an odd numbers
# Create board and fill with tiles from tile bag
board_dim = Dimensions(15, 15)
board = Board(board_dim, tile_bag=tile_bag)

# Set (board) view dimensions in tiles using Position - must be an odd numbers
# Set shift to centre view in the middle of the full boaes
# Create display
view_dim = Dimensions(9, 9)
shift_pos = Position((board.w - view_dim.w) // 2, (board.h - view_dim.h) // 2)
plot = Plot(view_dim, board.dim, tile_size, shift_pos)
plot.show_all_tiles(board.placements, board.orientations, tile_set.tiles)

# Set player position to be in centre of the board
# Create player and plot on board
player_pos = Position(shift_pos.x + (view_dim.w // 2), shift_pos.y + (view_dim.h // 2))
player_name = "Bruce"
player_number = 1
player_colour = GREEN
floor_colour = tile_set.tiles[board.placements[player_pos.x, player_pos.y]].floor_colour
print(f"floor_colour: {floor_colour}")
player = Player(player_name, player_number, player_colour, player_pos, floor_colour)
plot.show_player(player)

# Initialise text output
text = Text()
print()
print(tile_set)
print(board)
print("Game Start")
text.player_state(player, plot, board, tile_set)

running = True
# Gaming loop
while running:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == RANDOM:
            random_event = random.choice([0])
            if random_event == 0:
                direction = random.choice(Position.DIRECTIONS)
                patch_len = 1
                if direction == Position.UP or direction == Position.DOWN:
                    patch_board_start = random.choice(range(board.h))
                elif direction == Position.RIGHT or direction == Position.LEFT:
                    patch_board_start = random.choice(range(board.w))
                plot.slide_tiles(
                    patch_board_start,
                    patch_len,
                    direction,
                    board,
                    tile_set.tiles,
                    tile_bag,
                    move_board=True,
                )
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in MOVE_KEYS:
                if event.key == pygame.K_UP:
                    direction = Position.UP
                elif event.key == pygame.K_LEFT:
                    direction = Position.LEFT
                elif event.key == pygame.K_DOWN:
                    direction = Position.DOWN
                elif event.key == pygame.K_RIGHT:
                    direction = Position.RIGHT

                next_position = player.pos.get_next(direction)

                orientation = board.orientations[player.pos.y, player.pos.x]
                placement = board.placements[player.pos.y, player.pos.x]
                tile = tile_set.tiles[placement]
                # no door in current room in direction of intended movement
                if not board.check_for_door(player.pos, direction, tile_set.tiles):
                    plot.bounce_player(player, direction, tile, orientation)
                # trying to move off edge of board
                elif (
                    next_position.x < 0
                    or next_position.y < 0
                    or next_position.x >= board.w
                    or next_position.y >= board.h
                ):
                    plot.bounce_player(player, direction, tile, orientation, next=True)
                # no door in next roon in direction of intended movement
                elif not board.check_for_door(
                    player.pos, direction, tile_set.tiles, next=True
                ):
                    plot.bounce_player(player, direction, tile, orientation, next=True)
                # movement is possible
                else:
                    plot.move_player(
                        player,
                        direction,
                        board.placements,
                        board.orientations,
                        tile_set.tiles,
                    )
                    player.pos.move(direction)

                text.player_state(player, plot, board, tile_set)

            elif event.key in ROTATE_KEYS:
                if event.key == pygame.K_z:
                    rotation = 1
                elif event.key == pygame.K_x:
                    rotation = -1
                plot.rotate_tile(player.pos, rotation)
                board.rotate_tile(player.pos, rotation)

                text.player_state(player, plot, board, tile_set)

pygame.quit()
sys.exit()
