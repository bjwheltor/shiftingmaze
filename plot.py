"""
Plot

History
17-Jul-2021 - Initial version
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
    def __init__(self, view_dim, board_dim, tile_size, shift_pos=None):
        """
        view_dim : Position
            dimensions of (board) view in tiles (x, y)
        board_dim : Position
            dimensions of (full) board in tiles (x, y)
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

        self.board_dim = board_dim
        self.board_w = self.board_dim.w
        self.board_h = self.board_dim.h
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

        self.tile_size = tile_size

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
        self.board = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.board.fill(self.board_colour)

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

    def get_plot_position(self, board_pos):
        """
        Take tile absolute position and convert to plot position

        Parameters:
            board_pos : Position
                (full) board position in tiles (x, y)

        Returns
            plot_pos : Position
                image position in pixels (x,y)
        """
        x = board_pos.x - self.shift_pos.x
        y = board_pos.y - self.shift_pos.y

        if x < 0 or y < 0 or x >= self.view_w or y >= self.view_h:
            return None
        else:
            return Position(x * self.tile_size, y * self.tile_size)

    def show_tile(self, number, board_pos, orientation, tiles):
        """
        Plot tile in position with orientation

        Parameters:
            tile_number : int
                Number of tile to be placed
            board_pos : Position
                (full) board position in tiles (x, y)
            tile_orientation : int
                Orientation of tile to be placed
            tiles : TileSet.tiles
                Tiles in use
        """
        image = tiles[number].image
        rotated_image = pygame.transform.rotate(image, orientation * 90)
        plot_pos = self.get_plot_position(board_pos)
        if plot_pos:
            self.board.blit(rotated_image, plot_pos.coords())
            pygame.display.flip()

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

    def show_all_tiles(self, placements, orientations, tiles):
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
        """
        for board_x, board_y in np.ndindex(placements.shape):
            self.show_tile(
                placements[board_y, board_x],
                Position(board_x, board_y),
                orientations[board_y, board_x],
                tiles,
            )

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

        plot_pos = self.get_plot_position(board_pos)
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

    def show_player(self, player, player_offset=None):
        """
        Plot player in position

        Parameters:
            player: Player
                player instance

        Keywords:
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        plot_pos = self.get_plot_position(player.pos)

        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.w) / 2),
                int((self.tile_size - player.rect.h) / 2),
            )

        x = plot_pos.x + player_offset.x
        y = plot_pos.y + player_offset.y

        background_rect = pygame.Rect(x, y, player.size, player.size)
        player.background.blit(self.board, (0, 0), background_rect)

        self.board.blit(player.image, (x, y))
        pygame.display.flip()

    def move_player_free(self, player, direction, player_offset=None):
        """
        Move player in direction specified, as free move

        Parameters:
            player: Player
                player instance
            direction : int
                direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right

        Keywords:
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        plot_pos = self.get_plot_position(player.pos)
        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.w) / 2),
                int((self.tile_size - player.rect.h) / 2),
            )
        player_x = plot_pos.x + player_offset.x
        player_y = plot_pos.y + player_offset.y

        background_w = self.tile_size
        background_h = self.tile_size
        background_x = plot_pos.x
        background_y = plot_pos.y
        player_offset_x = player_offset.x
        player_offset_y = player_offset.y

        if direction == Position.DOWN or direction == Position.UP:
            background_h *= 2
        elif direction == Position.RIGHT or direction == Position.LEFT:
            background_w *= 2

        if direction == Position.UP:
            background_y -= self.tile_size
            player_offset_y += self.tile_size
        elif direction == Position.LEFT:
            background_x -= self.tile_size
            player_offset_x += self.tile_size

        background_tiles = pygame.Surface((background_w, background_h), pygame.SRCALPHA)
        background_rect = pygame.Rect(
            background_x, background_y, background_w, background_h
        )
        background_tiles.blit(self.board, (0, 0), background_rect)
        background_tiles.blit(player.background, (player_offset_x, player_offset_y))

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
        player_offset=None,
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
        Keywords:
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        plot_pos = self.get_plot_position(player.pos)
        if not player_offset:
            player_offset = Position(
                (self.tile_size - player.rect.w) // 2,
                (self.tile_size - player.rect.h) // 2,
            )
        player_x = plot_pos.x + player_offset.x
        player_y = plot_pos.y + player_offset.y

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

    def bounce_player(
        self, player, direction, tile, orientation, next=None, player_offset=None
    ):
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
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        plot_pos = self.get_plot_position(player.pos)
        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.w) / 2),
                int((self.tile_size - player.rect.h) / 2),
            )
        x = plot_pos.x + player_offset.x
        y = plot_pos.y + player_offset.y

        background_tile = pygame.transform.rotate(tile.image, orientation * 90)

        if direction == Position.UP:
            distance = player_offset.y
        elif direction == Position.DOWN:
            distance = self.tile_size - player.size - player_offset.y
        elif direction == Position.LEFT:
            distance = player_offset.x
        elif direction == Position.RIGHT:
            distance = self.tile_size - player.size - player_offset.x

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
        self,
        patch_board_start,
        patch_len,
        direction,
        board,
        tiles,
        tile_bag,
        move_board=False,
    ):
        """
        Slide a section of the board in specificed direction

        Parameters:
            patch_board_start : int
                (full) board x or y (tile) coordinate (depending on direction) of start of patch
             patch_len: int
                (tile) coordinate w or h length (depending on direction) of patch
            direction : int
                direction in dimich presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            board : Board
                tile board information
            tiles : TileSet.tiles
                dictionary of tiles indexed by the tile number
            tile_bag : TileBag
                bag of tiles from which random ones can be drawn
        """
        if direction == Position.RIGHT or direction == Position.LEFT:
            patch_board_x = -1
            patch_board_y = patch_board_start
            patch_board_w = board.w + 2
            patch_board_h = patch_len
        elif direction == Position.UP or direction == Position.DOWN:
            patch_board_x = patch_board_start
            patch_board_y = -1
            patch_board_w = patch_len
            patch_board_h = board.h + 2

        patch_placements = np.empty([patch_board_h, patch_board_w], dtype=int)
        patch_orientations = np.empty([patch_board_h, patch_board_w], dtype=int)

        plot_patch = pygame.Surface(
            (
                patch_board_w * self.tile_size,
                patch_board_h * self.tile_size,
            ),
            pygame.SRCALPHA,
        )

        for board_x in range(patch_board_x, patch_board_x + patch_board_w):
            for board_y in range(patch_board_y, patch_board_y + patch_board_h):
                patch_x = board_x - patch_board_x
                patch_y = board_y - patch_board_y
                if (
                    board_x < 0
                    or board_y < 0
                    or board_x >= board.w
                    or board_y >= board.h
                ):
                    patch_placements[patch_y, patch_x] = tile_bag.draw_tile()
                    patch_orientations[patch_y, patch_x] = random.choice([0, 1, 2, 3])
                else:
                    patch_placements[patch_y, patch_x] = board.placements[
                        board_y, board_x
                    ]
                    patch_orientations[patch_y, patch_x] = board.orientations[
                        board_y, board_x
                    ]

                tile_image = tiles[patch_placements[patch_y, patch_x]].image
                rotated_tile_image = pygame.transform.rotate(
                    tile_image, patch_orientations[patch_y, patch_x] * 90
                )
                patch_plot_x = patch_x * self.tile_size
                patch_plot_y = patch_y * self.tile_size
                plot_patch.blit(rotated_tile_image, (patch_plot_x, patch_plot_y))

        plot_x = (patch_board_x - self.shift_pos.x) * self.tile_size
        plot_y = (patch_board_y - self.shift_pos.y) * self.tile_size

        for move in range(self.tile_size):
            if direction == Position.RIGHT:
                plot_x += 1
            elif direction == Position.LEFT:
                plot_x -= 1
            elif direction == Position.DOWN:
                plot_y += 1
            elif direction == Position.UP:
                plot_y -= 1
            self.board.blit(plot_patch, (plot_x, plot_y))
            pygame.display.flip()
            pygame.time.delay(5)

        if move_board:
            if direction == Position.RIGHT:
                pos = Position(0, patch_board_y)
                placements = patch_placements[:, : board.w]
                orientations = patch_orientations[:, : board.w]
            elif direction == Position.LEFT:
                pos = Position(0, patch_board_y)
                placements = patch_placements[:, 2:]
                orientations = patch_orientations[:, 2:]
            elif direction == Position.UP:
                pos = Position(patch_board_x, 0)
                placements = patch_placements[2:, :]
                orientations = patch_orientations[2:, :]
            elif direction == Position.DOWN:
                pos = Position(patch_board_x, 0)
                placements = patch_placements[: board.h, :]
                orientations = patch_orientations[: board.h, :]
            print()
            print(f"Patch: pos = {pos}    direction = {direction}")
            print(patch_placements)
            print()
            board.apply_patch(pos, placements, orientations)

        # NEED TO ADD TILE RECYCING


#
# Some tests in isolation
#
if __name__ == "__main__":
    # extra imports for testing and initialise
    from player import *
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
    plot = Plot(view_dim, board.dim, tile_size, shift_pos)
    plot.show_all_tiles(board.placements, board.orientations, tile_set.tiles)

    #
    # Start Testing
    # print tile set and board set-up for reference
    print()
    print(tile_set)
    print(board)

    # test slide_tiles
    patch_board_start = 1
    patch_len = 1
    for direction in [0, 0, 0, 1, 1, 1]:
        plot.slide_tiles(
            patch_board_start,
            patch_len,
            direction,
            board,
            tile_set.tiles,
            tile_bag,
            move_board=True,
        )
        print()
        print(board)
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
