"""
Plot

History
17-Jul-2021 - Initial version
16-Sep-2021 - Separation of concerns - updated to focus plot on key functionality
"""
import os
import sys
from numpy.core.fromnumeric import nonzero
import pygame
import numpy as np

from tiles import *
from board import *
from position import *
from player import *


class Plot:
    def __init__(self, view_dim, placements, tiles, shift_pos=None):
        """
        view_dim : Position
            dimensions of (board) view in tiles (x, y)
        placements : numpy.array(h, w, n)
            holds all information on the state of the each square on the board.
            h is the y dimension
            w is the x dimension
            n is the board square attribute:
        tile_size : integer
            Length of one edge of a square tile

        Keywords:
            shift_pos : Position
                x-y movement vector for viewing area relative to dimole board (in 'tile space')
        """
        self.view_dim = view_dim
        self.view_w = self.view_dim.w
        self.view_h = self.view_dim.h
        self.view_half_w = self.view_w // 2
        self.view_half_h = self.view_h // 2

        #### NEW CODE
        self.board_h = placements.shape[0]
        self.board_w = placements.shape[1]
        self.n = placements.shape[2]
        self.board_dim = Dimensions(self.board_w, self.board_h)
        ###
        self.board_half_w = self.board_w // 2
        self.board_half_h = self.board_h // 2
        self.board_mid_pos = Position(self.board_half_w, self.board_half_h)

        self.centred_move_rect = pygame.Rect(
            self.view_half_w,
            self.view_half_h,
            self.board_w - self.view_w + 1,
            self.board_h - self.view_h + 1,
        )

        if shift_pos:
            self.shift_pos = shift_pos
        else:
            self.shift_pos = Position(0, 0)

        self.tile_size = tiles[0].size

        self.plot_w = self.view_w * self.tile_size
        self.plot_h = self.view_h * self.tile_size
        self.plot_dim = Dimensions(self.plot_w, self.plot_h)

        self.board_colour = (0, 0, 0)  # BLACK
        self.tile_colour = (150, 150, 255)  # BLUE

        # create empty tile space
        self.empty_tile = pygame.Surface(
            (self.tile_size, self.tile_size), pygame.SRCALPHA
        )
        self.empty_tile.fill(self.board_colour)

        # screen set-up
        SCREEN_X_ORIGIN = 0
        SCREEN_Y_ORIGIN = 0
        SCREEN_WIDTH = self.plot_w
        SCREEN_HEIGHT = self.plot_h

        os.environ["SDL_VIDEO_WINDOW_POS"] = (
            str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
        )

        # display tiles
        self.board = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        patch_view_placements = np.empty([self.view_h, self.view_w, self.n], dtype=int)
        patch_view_placements[...] = placements[
            self.shift_pos.y : self.shift_pos.y + self.view_h,
            self.shift_pos.x : self.shift_pos.x + self.view_h,
            :,
        ]
        patch = self.get_patch(patch_view_placements, tiles)
        print(f"self.shift_pos: {self.shift_pos}")
        self.board.blit(patch, (0, 0))

        pygame.display.flip()
        pygame.display.set_caption("Shifting Maze")

    def sign(self, x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return x

    def get_plot_pos(self, board_pos, shift_pos=None, offset=None):
        """
        Take tile absolute position and convert to plot position

        Parameters:
            board_pos : Position
                (full) board position in tiles (x, y)

        Returns
            plot_pos : Position
                image position in pixels (x,y)
        """
        if shift_pos is None:
            shift_pos = Position(0, 0)
        if offset is None:
            offset = Position(0, 0)
        plot_pos = Position(
            (board_pos.x - shift_pos.x) * self.tile_size + offset.x,
            (board_pos.y - shift_pos.y) * self.tile_size + offset.y,
        )
        return plot_pos

    def get_extra_tiles(
        self,
        placements,
        orientations,
        tiles,
        row_selection=None,
        column_selection=None,
    ):
        """
        Plot tile in position with orientation

        Parameters:
            placements : numpy.array(width, height)
                Tile number at each position of the board
            orientations : numpy.array(width, height)
                Orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
            row_selection : int
                If not None then indicates y coordinate of row to be returned
                (e.g. -1 for row above (board) view, self.view_h for row below board)
            column_selection : int
                If not None then indicates x coordinate of column to be returned
                (e.g. -1 for column to left of (board) view, self.view_w for column to right of board)

        Returns
            extra_tiles : pygame.Surface
                Image of row or column with the required tile images
        """
        row_length = 1
        column_length = 1
        if row_selection is not None:
            row_length = self.view_w
            column_selection = 0
        elif column_selection is not None:
            column_length = self.view_h
            row_selection = 0

        extra_tiles = pygame.Surface(
            (row_length * self.tile_size, column_length * self.tile_size),
            pygame.SRCALPHA,
        )

        for x in range(row_length):
            for y in range(column_length):
                board_x = x + self.shift_pos.x + column_selection
                board_y = y + self.shift_pos.y + row_selection
                number = placements[board_y, board_x]
                image = tiles[number].image
                orientation = orientations[board_y, board_x]
                rotated_image = pygame.transform.rotate(image, orientation * 90)
                extra_tiles.blit(
                    rotated_image, (x * self.tile_size, y * self.tile_size)
                )

        return extra_tiles

    def get_patch(self, placements, tiles):
        """
        Plot tile in position with orientation on surface

        Parameters:
            placements : numpy.array(h, w, n)
                holds all information on the state of the each square for patch
            tiles : TileSet.tiles
                Tiles in use

        Returns
            patch : pygame.Surface
                image of the patch tiles
        """
        h = placements.shape[0]
        w = placements.shape[1]

        patch = pygame.Surface(
            (w * self.tile_size, h * self.tile_size), pygame.SRCALPHA
        )

        for y in range(h):
            print(f"\n{y}")
            for x in range(w):
                print(f"    {x}")
                plot_pos = self.get_plot_pos(Position(x, y))
                print(f"        {plot_pos}")
                tile_image = tiles[placements[y, x, Board.TILE]].image
                rotated_tile_image = pygame.transform.rotate(
                    tile_image, placements[y, x, Board.ROT] * 90
                )
                patch.blit(rotated_tile_image, plot_pos.coords())
        return patch

    def rotate_tile(self, board_pos, rotation):
        """
        Plot tile in position with orientation

        Parameters:
            board_pos : Position
                (full) board position in tiles (x, y)
            rotation : int
                rotation to be applied to tile. Either +1 or -1.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        print(f"Action: Rotate tile   rotation: {rotation}")

        start_angle = 0
        end_angle = rotation * 90
        angle_inc = self.sign(end_angle - start_angle)
        end_angle += angle_inc

        plot_pos = self.get_plot_position(board_pos, shift_pos=self.shift_pos)
        if not plot_pos:
            return

        # extract tile from the board
        tile_rect = pygame.Rect(plot_pos.x, plot_pos.y, self.tile_size, self.tile_size)
        image = pygame.Surface(tile_rect.size, pygame.SRCALPHA)
        image.blit(self.board, (0, 0), tile_rect)
        image_rect = image.get_rect()

        left_row_rect = pygame.Rect(
            0, plot_pos.y, plot_pos.x + self.tile_size, self.tile_size
        )
        left_row = pygame.Surface(left_row_rect.size)
        left_row.blit(self.board, (0, 0), left_row_rect)
        left_row.blit(self.empty_tile, (plot_pos.x, 0))

        right_row_rect = pygame.Rect(
            plot_pos.x,
            plot_pos.y,
            self.plot_w - plot_pos.x + self.tile_size,
            self.tile_size,
        )
        right_row = pygame.Surface(right_row_rect.size)
        right_row.blit(self.board, (0, 0), right_row_rect)
        right_row.blit(self.empty_tile, (0, 0))

        top_column_rect = pygame.Rect(
            plot_pos.x, 0, self.tile_size, plot_pos.y + self.tile_size
        )
        top_column = pygame.Surface(top_column_rect.size)
        top_column.blit(self.board, (0, 0), top_column_rect)
        top_column.blit(self.empty_tile, (0, plot_pos.y))

        bottom_column_rect = pygame.Rect(
            plot_pos.x,
            plot_pos.y,
            self.tile_size,
            self.plot_h - plot_pos.y + self.tile_size,
        )
        bottom_column = pygame.Surface(bottom_column_rect.size)
        bottom_column.blit(self.board, (0, 0), bottom_column_rect)
        bottom_column.blit(self.empty_tile, (0, 0))

        for angle in range(start_angle, end_angle, angle_inc):

            rotated_image = pygame.transform.rotate(image, angle)
            rotated_image_rect = rotated_image.get_rect()

            rotate_adjust_x = (rotated_image_rect.right - image_rect.right) / 2
            rotate_adjust_y = (rotated_image_rect.bottom - image_rect.bottom) / 2

            self.board.blit(
                left_row, (left_row_rect.left - rotate_adjust_x, left_row_rect.top)
            )
            self.board.blit(
                right_row, (right_row_rect.left + rotate_adjust_x, right_row_rect.top)
            )
            self.board.blit(
                top_column,
                (top_column_rect.left, top_column_rect.top - rotate_adjust_y),
            )
            self.board.blit(
                bottom_column,
                (bottom_column_rect.left, bottom_column_rect.top + rotate_adjust_y),
            )
            self.board.blit(
                rotated_image,
                (plot_pos.x - rotate_adjust_x, plot_pos.y - rotate_adjust_y),
            )

            pygame.display.flip()
            pygame.time.delay(5)

    def show_player(self, player):
        """
        Plot player in position

        Parameters:
            player: Player
                player instance
        """
        plot_pos = self.get_plot_pos(player.pos, shift_pos=self.shift_pos)

        x = plot_pos.x + player.offset.x
        y = plot_pos.y + player.offset.y

        background_rect = pygame.Rect(x, y, player.size, player.size)
        player.background.blit(self.board, (0, 0), background_rect)

        self.board.blit(player.image, (x, y))
        pygame.display.flip()

    def move_player_free(self, player, direction):
        """
        Move player in direction specified, as free move

        Parameters:
            player: Player
                player instance
            direction : int
                direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
        """
        plot_pos = self.get_plot_position(player.pos, shift_pos=self.shift_pos)

        player_x = plot_pos.x + player.offset.x
        player_y = plot_pos.y + player.offset.y

        background_w = self.tile_size
        background_h = self.tile_size
        background_x = plot_pos.x
        background_y = plot_pos.y

        if direction == Position.DOWN or direction == Position.UP:
            background_h *= 2
        elif direction == Position.RIGHT or direction == Position.LEFT:
            background_w *= 2

        if direction == Position.UP:
            background_y -= self.tile_size
            player.offset.y += self.tile_size
        elif direction == Position.LEFT:
            background_x -= self.tile_size
            player.offset.x += self.tile_size

        background_tiles = pygame.Surface((background_w, background_h), pygame.SRCALPHA)
        background_rect = pygame.Rect(
            background_x, background_y, background_w, background_h
        )
        background_tiles.blit(self.board, (0, 0), background_rect)
        background_tiles.blit(player.background, (player.offset.x, player.offset.y))

        for move in range(0, self.tile_size + 1):
            self.board.blit(background_tiles, (background_x, background_y))
            if direction == Position.DOWN:
                self.board.blit(player.image, (player_x, player_y + move))
            elif direction == Position.UP:
                self.board.blit(player.image, (player_x, player_y - move))
            elif direction == Position.RIGHT:
                self.board.blit(player.image, (player_x + move, player_y))
            elif direction == Position.LEFT:
                self.board.blit(player.image, (player_x - move, player_y))
            pygame.display.flip()

    def move_player_centred(
        self,
        player,
        direction,
        placements,
        orientations,
        tiles,
    ):
        """
        Move player in direction specified, but maintain in centre of board.
        i.e. the board appears to move rather than then player.

        Parameters:
            player: Player
                player instance
            direction : int
                direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            placements : numpy.array(width, height)
                tile number at each position of the board
            orientations : numpy.array(width, height)
                orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
        """
        plot_pos = self.get_plot_position(player.pos, shift_pos=self.shift_pos)

        player_x = plot_pos.x + player.offset.x
        player_y = plot_pos.y + player.offset.y

        background_w = self.plot_w
        background_h = self.plot_h
        plot_offset_x = 0
        plot_offset_y = 0
        row_selection = None
        column_selection = None

        if direction == Position.RIGHT or direction == Position.LEFT:
            background_w += self.tile_size
        elif direction == Position.DOWN or direction == Position.UP:
            background_h += self.tile_size

        if direction == Position.UP:
            plot_offset_y = self.tile_size
            row_selection = -1
        elif direction == Position.LEFT:
            plot_offset_x = self.tile_size
            column_selection = -1
        elif direction == Position.DOWN:
            row_selection = self.view_h
        elif direction == Position.RIGHT:
            column_selection = self.view_w

        background_tiles = pygame.Surface((background_w, background_h), pygame.SRCALPHA)
        self.board.blit(player.background, (player_x, player_y))
        background_tiles.blit(self.board, (plot_offset_x, plot_offset_y))

        extra_tiles = self.get_extra_tiles(
            placements,
            orientations,
            tiles,
            row_selection=row_selection,
            column_selection=column_selection,
        )
        if direction == Position.UP or direction == Position.LEFT:
            background_tiles.blit(extra_tiles, (0, 0))
        elif direction == Position.DOWN:
            background_tiles.blit(extra_tiles, (0, self.view_h * self.tile_size))
        elif direction == Position.RIGHT:
            background_tiles.blit(extra_tiles, (self.view_w * self.tile_size, 0))

        for move in range(0, self.tile_size + 1):
            if direction == Position.DOWN:
                self.board.blit(background_tiles, (0, -move))
            elif direction == Position.UP:
                self.board.blit(background_tiles, (0, move - plot_offset_y))
            elif direction == Position.RIGHT:
                self.board.blit(background_tiles, (-move, 0))
            elif direction == Position.LEFT:
                self.board.blit(background_tiles, (move - plot_offset_x, 0))
            self.board.blit(player.image, (player_x, player_y))
            pygame.display.flip()

    def move_player(self, player, direction, placements, orientations, tiles):
        """
        Move player in direction specified, deciding dimether to keep centred of freely move

        Parameters:
            player: Player
                player instance
            direction : int
                Direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            placements : numpy.array(width, height)
                tile number at each position of the board
            orientations : numpy.array(width, height)
                orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
        """

        if (
            (direction == Position.LEFT or direction == Position.RIGHT)
            and self.centred_move_rect.collidepoint(player.pos.x, self.board_mid_pos.y)
            and self.centred_move_rect.collidepoint(
                player.pos.get_next(direction).x, self.board_mid_pos.y
            )
        ) or (
            (direction == Position.UP or direction == Position.DOWN)
            and self.centred_move_rect.collidepoint(self.board_mid_pos.x, player.pos.y)
            and self.centred_move_rect.collidepoint(
                self.board_mid_pos.x, player.pos.get_next(direction).y
            )
        ):
            print(f"Action: Move (centred)    direction: {direction}")
            self.move_player_centred(player, direction, placements, orientations, tiles)
            self.shift_pos.move(direction)
        else:
            print(f"Action: Move (free)    direction: {direction}")
            self.move_player_free(player, direction)

    def bounce_player(self, player, direction, tile, orientation, next=None):
        """
        Move player in direction specified, deciding dimether to keep centred of freely move

        Parameters:
            player: Player
                player instance
            direction : int
                direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            tile : Tile
               current tile occupied by player

        Keywords:
            next : logical
                if true check for door coming from next tile
        """
        plot_pos = self.get_plot_position(player.pos, shift_pos=self.shift_pos)

        x = plot_pos.x + player.offset.x
        y = plot_pos.y + player.offset.y

        background_tile = pygame.transform.rotate(tile.image, orientation * 90)

        if direction == Position.UP:
            distance = player.offset.y
        elif direction == Position.DOWN:
            distance = self.tile_size - player.size - player.offset.y
        elif direction == Position.LEFT:
            distance = player.offset.x
        elif direction == Position.RIGHT:
            distance = self.tile_size - player.size - player.offset.x

        if not next:
            distance -= tile.wall_width

        for move in range(0, distance):
            self.board.blit(background_tile, plot_pos.coords())
            if direction == Position.DOWN:
                self.board.blit(player.image, (x, y + move))
            elif direction == Position.UP:
                self.board.blit(player.image, (x, y - move))
            elif direction == Position.RIGHT:
                self.board.blit(player.image, (x + move, y))
            elif direction == Position.LEFT:
                self.board.blit(player.image, (x - move, y))
            pygame.display.flip()

        for move in range(distance, 0, -1):
            self.board.blit(background_tile, plot_pos.coords())
            if direction == Position.DOWN:
                self.board.blit(player.image, (x, y + move))
            elif direction == Position.UP:
                self.board.blit(player.image, (x, y - move))
            elif direction == Position.RIGHT:
                self.board.blit(player.image, (x + move, y))
            elif direction == Position.LEFT:
                self.board.blit(player.image, (x - move, y))
            pygame.display.flip()

    def slide_tiles(
        self, patch_placements, dir, row_or_col, tiles, player=None, move_player=0
    ):
        """
        Slide a section of the board in specificed direction

        Parameters:
            patch_placements : numpy.array(h, w, n)
                holds all information on the state of the each square on the board.in the 'patch'.
                The coordinates are full board and describe the patch over the full board,
                not just the view of the board.
            dir : int
                direction in dimich presence of door to be checked.
                0 = UP, 1 = LEFT, 2 = DOWN, 3 = RIGHT
            row_or_col : int
                (full) board x or y (tile) coordinate
            tiles : TileSet.tiles
                dictionary of tiles indexed by the tile number

        Keywords
            player : Player
                player information, provided if required
            move_player : int
                indicates if and how player position is handled in plotting:
                0 = DO_NOT_MOVE - no re-plotting of player
                1 = MOVE_WITH_TILES - player is plotted on patch and moved with it
                2 = STAY_AS_TILES_MOVE - player stays still as tiles move beneath
        """
        patch_h = patch_placements.shape[0]
        patch_w = patch_placements.shape[1]
        patch_n = patch_placements.shape[2]

        if (
            move_player == Player.MOVE_WITH_TILES
            or move_player == Player.STAY_AS_TILES_MOVE
        ):
            player_plot_pos = self.get_plot_pos(
                player.pos, shift_pos=self.shift_pos, offset=player.offset
            )

        # Extract the viewable patch placements from the full board placements
        # and generates patch
        if dir == Position.RIGHT or dir == Position.LEFT:
            patch_view_h = patch_h
            patch_view_w = self.view_w + 1
            patch_view_placements = np.empty(
                [patch_view_h, patch_view_w, patch_n], dtype=int
            )
            patch_view_placements[...] = patch_placements[
                :, self.shift_pos.x : self.shift_pos.x + self.view_w + 1, :
            ]
        elif dir == Position.UP or dir == Position.DOWN:
            patch_view_h = self.view_h + 1
            patch_view_w = patch_w
            patch_view_placements = np.empty(
                [patch_view_h, patch_view_w, patch_n], dtype=int
            )
            patch_view_placements[...] = patch_placements[
                self.shift_pos.y : self.shift_pos.y + self.view_h + 1, ...
            ]

        patch = self.get_patch(patch_view_placements, tiles)

        # Calculate the initial plot coordinates for the patch
        if dir == Position.RIGHT:
            plot_x = -1 * self.tile_size
            plot_y = (row_or_col - self.shift_pos.y) * self.tile_size
        elif dir == Position.LEFT:
            plot_x = 0
            plot_y = (row_or_col - self.shift_pos.y) * self.tile_size
        elif dir == Position.DOWN:
            plot_x = (row_or_col - self.shift_pos.x) * self.tile_size
            plot_y = -1 * self.tile_size
        elif dir == Position.UP:
            plot_x = (row_or_col - self.shift_pos.x) * self.tile_size
            plot_y = 0

        delta_plot_x = 0
        delta_plot_y = 0

        # Slide the patch, overplotting the player if required
        for move in range(self.tile_size):
            if dir == Position.RIGHT:
                delta_plot_x = move
            elif dir == Position.LEFT:
                delta_plot_x = -move
            elif dir == Position.DOWN:
                delta_plot_y = move
            elif dir == Position.UP:
                delta_plot_y = -move
            self.board.blit(patch, (plot_x + delta_plot_x, plot_y + delta_plot_y))
            if move_player == Player.MOVE_WITH_TILES:
                self.board.blit(
                    player.image,
                    (
                        player_plot_pos.x + delta_plot_x,
                        player_plot_pos.y + delta_plot_y,
                    ),
                )
            elif move_player == Player.STAY_AS_TILES_MOVE:
                self.board.blit(player.image, player_plot_pos.coords())

            pygame.display.flip()
            pygame.time.delay(5)


# ===============================
# Some tests in isolation
# ===============================
if __name__ == "__main__":
    # extra imports for testing and initialise
    from text import *

    pygame.init()

    # Define colours
    GREEN = (100, 200, 100)

    MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
    ROTATE_KEYS = (pygame.K_z, pygame.K_x)
    SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
    SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)

    # Create a tile set and fixed tile list
    tileset_name = "test"
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
    tile_list = (
        [1, 1, 1, 4, 4]
        + [1, 0, 0, 0, 4]
        + [2, 0, 0, 0, 4]
        + [2, 0, 0, 0, 3]
        + [2, 2, 3, 3, 3]
    )

    # Set (full) board dimensions in tiles using Position - must be an odd numbers
    # Create board and fill with tiles from tile bag
    board_dim = Dimensions(5, 5)
    board = Board(board_dim, tile_list=tile_list)

    # Set (board) view dimensions in tiles using Position - must be an odd numbers
    # Set shift to centre view in the middle of the full boaes
    # Create display
    view_dim = Dimensions(3, 3)
    shift_pos = Position((board.w - view_dim.w) // 2, (board.h - view_dim.h) // 2)
    plot = Plot(view_dim, board.placements, tile_set.tiles, shift_pos=shift_pos)

    # Set player position to be in centre of the board
    # Create player and plot on board
    player_pos = Position(
        shift_pos.x + (view_dim.w // 2), shift_pos.y + (view_dim.h // 2)
    )
    player_name = "Bruce"
    player_number = 1
    player_colour = GREEN
    start_tile = tile_set.tiles[0]

    player = Player(player_name, player_number, player_colour, player_pos, start_tile)
    plot.show_player(player)

    pygame.time.delay(1000)

    #
    # Start Testing
    # print tile set and board set-up for reference
    print()
    print(tile_set)
    print(board)

    # Test for sliding rows and columns
    # Right
    row = 2
    dir = Position.RIGHT
    print("\nSlide row")
    print(f"row: {row}  dir: {dir}")
    patch_placements = board.slide_row(row, dir, tile_bag)
    print(board)
    plot.slide_tiles(
        patch_placements,
        dir,
        row,
        tile_set.tiles,
        player,
        move_player=Player.MOVE_WITH_TILES,
    )
    player.pos.move(dir)
    pygame.time.delay(1000)
    # Left
    row = 2
    dir = Position.LEFT
    print("\nSlide row")
    print(f"row: {row}  dir: {dir}")
    patch_placements = board.slide_row(row, dir, tile_bag)
    print(board)
    plot.slide_tiles(
        patch_placements,
        dir,
        row,
        tile_set.tiles,
        player,
        move_player=Player.MOVE_WITH_TILES,
    )
    player.pos.move(dir)
    pygame.time.delay(1000)
    # Down
    row = 2
    dir = Position.DOWN
    print("\nSlide row")
    print(f"row: {row}  dir: {dir}")
    patch_placements = board.slide_col(row, dir, tile_bag)
    print(board)
    plot.slide_tiles(
        patch_placements,
        dir,
        row,
        tile_set.tiles,
        player,
        move_player=Player.MOVE_WITH_TILES,
    )
    player.pos.move(dir)
    pygame.time.delay(1000)
    # Up
    row = 2
    dir = Position.UP
    print("\nSlide row")
    print(f"row: {row}  dir: {dir}")
    patch_placements = board.slide_col(row, dir, tile_bag)
    print(board)
    plot.slide_tiles(
        patch_placements,
        dir,
        row,
        tile_set.tiles,
        player,
        move_player=Player.MOVE_WITH_TILES,
    )
    player.pos.move(dir)

    # hold screen until escaped
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()
    sys.exit()
