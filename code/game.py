"""
Main game control code

History
24-Jul-2021 - Initial version
21-Aug-2021 - Simplified control
"""
import os
import sys
import pygame
import numpy as np

from position import *
from direction import *
from tile import *
from tileset import *
from tilebag import *
from player import *
from board import *
from plot import *
from text import *

# initiate pygame
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

# Input keys
MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
ROTATE_KEYS = (pygame.K_z, pygame.K_x)
SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)


# Set up random events
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

# Set up dimensions of board and view
board_width = 7
board_height = 7
view_width = 5
view_height = 5
view_left = (board_width - view_width) // 2
view_top = (board_height - view_height) // 2
view_rect = pygame.Rect(view_left, view_top, view_width, view_height)

# Create board and fill with tiles from tile bag
board = Board(board_width, board_height, tile_bag=tile_bag)

# Set up screen display
SCREEN_X_ORIGIN = 0
SCREEN_Y_ORIGIN = 0
SCREEN_WIDTH = view_width * tile_size
SCREEN_HEIGHT = view_height * tile_size
os.environ["SDL_VIDEO_WINDOW_POS"] = str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Shifting Maze")

# Set-up view on board
view = View(view_rect, board.placements, tile_set.tiles)


# Set (board) view dimensions in tiles using Position - must be an odd numbers
# Set shift to centre view in the middle of the full boaes
# Create display
# view_dim = Dimensions(5, 5)
# shift_pos = Position((board.w - view_dim.w) // 2, (board.h - view_dim.h) // 2)
# plot = Plot(view_dim, board.placements, tile_set.tiles, shift_pos=shift_pos)

# Set player position to be in centre of the board
# Create player and plot on board
player_pos = Position(shift_pos.x + (view_dim.w // 2), shift_pos.y + (view_dim.h // 2))
player_name = "Bruce"
player_number = 1
player_colour = GREEN
start_tile = tile_set.tiles[0]

player = Player(player_name, player_number, player_colour, player_pos, start_tile)
plot.show_player(player)

# Initialise text output
text = Text()
print()
print(tile_set)
print(board)
print("Game Start")
text.player_state(player, plot, board, tile_set)

## NEW GAME LOOP CODE
running = True

while running:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key in MOVE_KEYS:

                tile = tile_set.tiles[
                    board.placements[player.pos.y, player.pos.x, Board.TILE]
                ]
                rot = board.placements[player.pos.y, player.pos.x, Board.ROT]

                if event.key == pygame.K_UP:
                    dir = Position.UP
                elif event.key == pygame.K_LEFT:
                    dir = Position.LEFT
                elif event.key == pygame.K_DOWN:
                    dir = Position.DOWN
                elif event.key == pygame.K_RIGHT:
                    dir = Position.RIGHT

                # moving off edge of board
                if plot.is_moving_off_board(player.pos, dir):
                    print(f"Bounce off edge of board - direction: {dir}")
                    plot.bounce_player_free(player, dir, tile, rot, next=True)
                # no door in current room in direction of intended movement
                # TODO: add centred bounce
                elif not board.check_for_door(player.pos, dir, tile_set.tiles):
                    print(f"Bounce off door in current room - direction: {dir}")
                    plot.bounce_player_free(player, dir, tile, rot)

                # no door in next roon in direction of intended movement
                # TODO: add centred bounce
                elif not board.check_for_door(
                    player.pos, dir, tile_set.tiles, next=True
                ):
                    print(f"Bounce off door in next room - direction: {dir}")
                    plot.bounce_player_free(player, dir, tile, rot, next=True)

                # movement is possible
                else:
                    if plot.is_centred_move(player.pos, dir):
                        print(f"Centred move - direction: {dir}")
                        plot.move_player_centred(
                            player, dir, board.placements, tile_set.tiles
                        )
                    else:
                        print(f"Free move - direction: {dir}")
                        plot.move_player_free(
                            player, dir, board.placements, tile_set.tiles
                        )
                    player.pos.move(dir)

            elif event.key in ROTATE_KEYS:
                if event.key == pygame.K_z:
                    rotation = 1
                elif event.key == pygame.K_x:
                    rotation = -1
                plot.rotate_tile(player.pos, rotation)
                board.rotate_tile(player.pos, rotation)

            tile = tile_set.tiles[
                board.placements[player.pos.y, player.pos.x, Board.TILE]
            ]
            rot = board.placements[player.pos.y, player.pos.x, Board.ROT]
            doors = tile.doors
            print(f"Player pos: {player.pos}    Plot shift pos: {plot.shift_pos}")
            print(f"Current tile: {tile.number} {doors}   rotation: {rot}\n")

        elif event.type == RANDOM:
            print(f"Random Event")
            random_event = random.choice([0])
            if random_event == 0:
                dir = random.choice(Position.DIRECTIONS)
                if dir == Position.RIGHT or dir == Position.LEFT:
                    row = random.choice(range(board.w))
                    # row not in view
                    if row < shift_pos.y or row > shift_pos.y + plot.view_h:
                        board.slide_row_free(col_or_row, dir, tile_bag)
                    # row on screen but player not on row
                    elif player.pos.y != row:
                        move_player = Player.DO_NOT_MOVE
                        plot.slide_row_free()
                    # player on row, but free move
                    elif not plot.is_centred_move(player.pos, dir):
                        move_player = Player.MOVE_WITH_TILES
                        plot.slide_row_free()
                    # player on row, centred move
                    else:
                        plot.slide_row_centred()

                if dir == Position.RIGHT or dir == Position.LEFT:
                    row = random.choice(range(shift_pos.y, shift_pos.y + plot.view_h))
                    print("\Slide row")
                    print(f"row: {col_or_row}  dir: {dir}")
                    patch_placements = board.slide_row(col_or_row, dir, tile_bag)
                    if player.pos.y == col_or_row:
                        move_player = Player.MOVE_WITH_TILES
                    else:
                        move_player = Player.DO_NOT_MOVE
                elif dir == Position.UP or dir == Position.DOWN:
                    col_or_row = random.choice(
                        range(shift_pos.x, shift_pos.x + plot.view_w)
                    )
                    print("Slide column")
                    print(f"col: {col_or_row}  dir: {dir}")
                    patch_placements = board.slide_col(col_or_row, dir, tile_bag)
                    if player.pos.x == col_or_row:
                        move_player = Player.MOVE_WITH_TILES
                    else:
                        move_player = Player.DO_NOT_MOVE
                print(board)
                plot.slide_tiles(
                    patch_placements,
                    dir,
                    col_or_row,
                    tile_set.tiles,
                    player,
                    move_player,
                )
                # Re-adjust view of board so player is in middle - need to:
                ## ADD CHECK FOR RE-CENTRING BEING SENSIBLE (i.e. shift_pos > 0)
                if move_player == Player.MOVE_WITH_TILES:
                    player.pos.move(dir)
                    dir_corr = (dir + 2) % 4
                    plot.move_player_centred(
                        player, dir_corr, board.placements, tile_set.tiles
                    )
                    plot.shift_pos.move(dir)

pygame.quit()
sys.exit()
