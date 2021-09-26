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
board_dim = Dimensions(7, 7)
board = Board(board_dim, tile_bag=tile_bag)

# Set (board) view dimensions in tiles using Position - must be an odd numbers
# Set shift to centre view in the middle of the full boaes
# Create display
view_dim = Dimensions(5, 5)
shift_pos = Position((board.w - view_dim.w) // 2, (board.h - view_dim.h) // 2)
plot = Plot(view_dim, board.placements, tile_set.tiles, shift_pos=shift_pos)

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


# Old Gaming loop code

running = True

while running:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == RANDOM:
            text.player_state(player, plot, board, tile_set)
            random_event = random.choice([0])
            if random_event == 0:
                dir = random.choice(Position.DIRECTIONS)
                if dir == Position.RIGHT or dir == Position.LEFT:
                    col_or_row = random.choice(
                        range(shift_pos.y, shift_pos.y + plot.view_h)
                    )
                    print("\nSlide row")
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
                    print("\nSlide column")
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
                        player, dir_corr, board.placements, tile_set.tiles, move_player
                    )
                    plot.shift_pos.move(dir)
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
