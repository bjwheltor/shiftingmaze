"""
Plot

History
17-Jul-2021 - Initial version
"""
import os
import sys
import random
import pygame
import numpy as np

from tiles import *
from board import *
from position import *


class Plot:
    def __init__(
        self,
        x_tiles,
        y_tiles,
        total_x_tiles,
        total_y_tiles,
        tile_size,
        position_shift=None,
    ):
        """

        Keywords:
            position_shift : int
                x-y movement vector for viewing area relative to whole board (in 'tile space')
        """
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles

        self.total_x_tiles = total_x_tiles
        self.total_y_tiles = total_y_tiles

        self.half_x_tiles = self.x_tiles // 2
        self.half_y_tiles = self.y_tiles // 2

        self.total_mid_point = Position(total_x_tiles // 2, total_y_tiles // 2)

        self.centred_move_rect = pygame.Rect(
            self.half_x_tiles,
            self.half_y_tiles,
            total_x_tiles - self.x_tiles + 1,
            total_y_tiles - self.y_tiles + 1,
        )

        if position_shift:
            self.position_shift = position_shift
        else:
            self.position_shift = Position(0, 0)

        self.tile_size = tile_size

        self.board_width = self.x_tiles * self.tile_size
        self.board_height = self.y_tiles * self.tile_size

        self.board_left = 0
        self.board_top = 0
        self.board_right = self.board_left + self.board_width
        self.board_bottom = self.board_top + self.board_height

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
        SCREEN_WIDTH = self.board_width
        SCREEN_HEIGHT = self.board_height

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

    def position_placed(self, tile_position):
        """ """
        x = tile_position.x - self.position_shift.x
        y = tile_position.y - self.position_shift.y

        if x < 0 or y < 0 or x >= self.x_tiles or y >= self.x_tiles:
            return None
        else:
            return Position(x * self.tile_size, y * self.tile_size)

    def show_tile(self, tile_number, tile_position, tile_orientation, tiles):
        """
        Plot tile in position with orientation

        Parameters:
            tile_number : int
                Number of tile to be placed
            tile_position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
            tile_orientation : int
                Orientation of tile to be placed
            tiles : TileSet.tiles
                Tiles in use
        """
        tile_image = tiles[tile_number].image
        tile_placed = pygame.transform.rotate(tile_image, tile_orientation * 90)
        position_placed = self.position_placed(tile_position)
        if position_placed:
            self.board.blit(tile_placed, (position_placed.x, position_placed.y))
            pygame.display.flip()

    def get_extra_tiles(
        self,
        tile_placements,
        tile_orientations,
        tiles,
        row_selection=None,
        column_selection=None,
    ):
        """
        Plot tile in position with orientation

        Parameters:
            tile_placements : numpy.array(width, height)
                Tile number at each position of the board
            tile_orientations : numpy.array(width, height)
                Orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
            row_selection : int
                If not None then indicates y coordinate of row to be returned
                (e.g. -1 for row above board, self.y_tiles+1 for row below board)
            column_selection : int
                If not None then indicates x coordinate of column to be returned
                (e.g. -1 for column to left of board, self.x_tiles+1 for column to right of board)

        Returns
            extra_tiles : pygame.Surface
                Image of row or column with the required tile images
        """
        row_length = 1
        column_length = 1
        if row_selection is not None:
            row_length = self.x_tiles
            column_selection = 0
        elif column_selection is not None:
            column_length = self.y_tiles
            row_selection = 0

        extra_tiles = pygame.Surface(
            (row_length * self.tile_size, column_length * self.tile_size),
            pygame.SRCALPHA,
        )

        for x in range(row_length):
            for y in range(column_length):
                tile_x = x + self.position_shift.x + column_selection
                tile_y = y + self.position_shift.y + row_selection
                tile_number = tile_placements[tile_x, tile_y]
                tile_image = tiles[tile_number].image
                tile_orientation = tile_orientations[tile_x, tile_y]
                tile_placed = pygame.transform.rotate(tile_image, tile_orientation * 90)
                extra_tiles.blit(tile_placed, (x * self.tile_size, y * self.tile_size))

        return extra_tiles

    def show_all_tiles(self, tile_placements, tile_orientations, tiles):
        """
        Plot tile in position with orientation

        Parameters:
            tile_placements : numpy.array(width, height)
                Tile number at each position of the board
            tile_orientations : numpy.array(width, height)
                Orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
        """
        for tile_x, tile_y in np.ndindex(tile_placements.shape):
            self.show_tile(
                tile_placements[tile_x, tile_y],
                Position(tile_x, tile_y),
                tile_orientations[tile_x, tile_y],
                tiles,
            )

    def rotate_tile(self, tile_position, rotation):
        """
        Plot tile in position with orientation

        Parameters:
            tile_position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
            rotation : int
                rotation to be applied to tile. Either +1 or -1.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        start_angle = 0
        end_angle = rotation * 90
        angle_inc = self.sign(end_angle - start_angle)
        end_angle += angle_inc

        position_placed = self.position_placed(tile_position)
        if not position_placed:
            return

        x = position_placed.x
        y = position_placed.y
        print(f"x = {x} y = {y}")

        # extract tile from the board
        tile_image_area = pygame.Rect(x, y, self.tile_size, self.tile_size)
        tile_image = pygame.Surface(tile_image_area.size, pygame.SRCALPHA)
        tile_image.blit(self.board, (0, 0), tile_image_area)
        tile_image_rect = tile_image.get_rect()

        left_row_rect = pygame.Rect(0, y, x + self.tile_size, self.tile_size)
        left_row = pygame.Surface(left_row_rect.size)
        left_row.blit(self.board, (0, 0), left_row_rect)
        left_row.blit(self.empty_tile, (x, 0))

        right_row_rect = pygame.Rect(
            x, y, self.board_width - x + self.tile_size, self.tile_size
        )
        right_row = pygame.Surface(right_row_rect.size)
        right_row.blit(self.board, (0, 0), right_row_rect)
        right_row.blit(self.empty_tile, (0, 0))

        top_column_rect = pygame.Rect(x, 0, self.tile_size, y + self.tile_size)
        top_column = pygame.Surface(top_column_rect.size)
        top_column.blit(self.board, (0, 0), top_column_rect)
        top_column.blit(self.empty_tile, (0, y))

        bottom_column_rect = pygame.Rect(
            x, y, self.tile_size, self.board_height - y + self.tile_size
        )
        bottom_column = pygame.Surface(bottom_column_rect.size)
        bottom_column.blit(self.board, (0, 0), bottom_column_rect)
        bottom_column.blit(self.empty_tile, (0, 0))

        for angle in range(start_angle, end_angle, angle_inc):

            tile_placed = pygame.transform.rotate(tile_image, angle)
            tile_placed_rect = tile_placed.get_rect()

            x_rot_adjust = (tile_placed_rect.right - tile_image_rect.right) / 2
            y_rot_adjust = (tile_placed_rect.bottom - tile_image_rect.bottom) / 2

            self.board.blit(
                left_row, (left_row_rect.left - x_rot_adjust, left_row_rect.top)
            )
            self.board.blit(
                right_row, (right_row_rect.left + x_rot_adjust, right_row_rect.top)
            )
            self.board.blit(
                top_column, (top_column_rect.left, top_column_rect.top - y_rot_adjust)
            )
            self.board.blit(
                bottom_column,
                (bottom_column_rect.left, bottom_column_rect.top + y_rot_adjust),
            )
            self.board.blit(tile_placed, (x - x_rot_adjust, y - y_rot_adjust))

            pygame.display.flip()
            pygame.time.delay(5)

    def slide_row(self, row_y, slide, fill_tile_image):
        """ """
        row_y -= self.position_shift.y

        if row_y < 0 or row_y >= self.x_tiles:
            return None

        y = row_y * self.tile_size

        extended_row = pygame.Surface(
            (self.board_width + self.tile_size, self.tile_size), pygame.SRCALPHA
        )

        row_rect = pygame.Rect(0, y, self.board_width, self.tile_size)

        if slide == "right":
            extended_row.blit(self.board, (0, 0), row_rect)
            extended_row.blit(fill_tile_image, (self.board_width, 0))
            for x in range(-self.tile_size, 1):
                self.board.blit(extended_row, (x, y))
                pygame.display.flip()

        elif slide == "left":
            extended_row.blit(self.board, (self.tile_size, 0))
            extended_row.blit(fill_tile_image, (0, 0), row_rect)
            for x in range(0, -self.tile_size - 1, -1):
                self.board.blit(extended_row, (x, y))
                pygame.display.flip()

    def slide_column(self, column_x, slide, fill_tile_image):
        """ """
        column_x -= self.position_shift.x

        if column_x < 0 or column_x >= self.x_tiles:
            return None

        x = column_x * self.tile_size

        extended_column = pygame.Surface(
            (self.tile_size, self.board_height + self.tile_size), pygame.SRCALPHA
        )

        column_rect = pygame.Rect(x, 0, self.tile_size, self.board_height)

        if slide == "down":
            extended_column.blit(self.board, (0, 0), column_rect)
            extended_column.blit(fill_tile_image, (0, self.board_height))
            for y in range(-self.tile_size, 1):
                self.board.blit(extended_column, (x, y))
                pygame.display.flip()

        elif slide == "up":
            extended_column.blit(self.board, (0, self.tile_size), column_rect)
            extended_column.blit(fill_tile_image, (0, 0))
            for y in range(0, -self.tile_size - 1, -1):
                self.board.blit(extended_column, (x, y))
                pygame.display.flip()

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
        position_placed = self.position_placed(player.position)

        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.width) / 2),
                int((self.tile_size - player.rect.height) / 2),
            )

        x = position_placed.x + player_offset.x
        y = position_placed.y + player_offset.y

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
                direction in which presence of door to be checked.
            0 = up, 1 = left, 2 = down, 3 = right

        Keywords:
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        position_placed = self.position_placed(player.position)
        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.width) / 2),
                int((self.tile_size - player.rect.height) / 2),
            )
        player_x = position_placed.x + player_offset.x
        player_y = position_placed.y + player_offset.y

        background_width = self.tile_size
        background_height = self.tile_size
        background_x = position_placed.x
        background_y = position_placed.y
        player_offset_x = player_offset.x
        player_offset_y = player_offset.y

        if direction == Position.DOWN or direction == Position.UP:
            background_height *= 2
        elif direction == Position.RIGHT or direction == Position.LEFT:
            background_width *= 2

        if direction == Position.UP:
            background_y -= self.tile_size
            player_offset_y += self.tile_size
        elif direction == Position.LEFT:
            background_x -= self.tile_size
            player_offset_x += self.tile_size

        background_tiles = pygame.Surface(
            (background_width, background_height), pygame.SRCALPHA
        )
        background_rect = pygame.Rect(
            background_x, background_y, background_width, background_height
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
        tile_placements,
        tile_orientations,
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
                direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            tile_placements : numpy.array(width, height)
                tile number at each position of the board
            tile_orientations : numpy.array(width, height)
                orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
        Keywords:
            player_offset : Position
                x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
        """
        position_placed = self.position_placed(player.position)
        if not player_offset:
            player_offset = Position(
                int((self.tile_size - player.rect.width) / 2),
                int((self.tile_size - player.rect.height) / 2),
            )
        player_x = position_placed.x + player_offset.x
        player_y = position_placed.y + player_offset.y

        background_width = self.board_width
        background_height = self.board_height
        board_offset_x = 0
        board_offset_y = 0
        row_selection = None
        column_selection = None

        if direction == Position.DOWN or direction == Position.UP:
            background_height += self.tile_size
        elif direction == Position.RIGHT or direction == Position.LEFT:
            background_width += self.tile_size

        if direction == Position.UP:
            board_offset_y = self.tile_size
            row_selection = -1
        elif direction == Position.LEFT:
            board_offset_x = self.tile_size
            column_selection = -1
        elif direction == Position.DOWN:
            row_selection = self.y_tiles - 1
        elif direction == Position.RIGHT:
            column_selection = self.x_tiles - 1

        background_tiles = pygame.Surface(
            (background_width, background_height), pygame.SRCALPHA
        )
        self.board.blit(player.background, (player_x, player_y))
        background_tiles.blit(self.board, (board_offset_x, board_offset_y))

        extra_tiles = self.get_extra_tiles(
            tile_placements,
            tile_orientations,
            tiles,
            row_selection=row_selection,
            column_selection=column_selection,
        )
        if direction == Position.UP or direction == Position.LEFT:
            background_tiles.blit(extra_tiles, (0, 0))
        elif direction == Position.DOWN:
            background_tiles.blit(extra_tiles, (0, self.y_tiles * self.tile_size))
        elif direction == Position.RIGHT:
            background_tiles.blit(extra_tiles, (self.x_tiles * self.tile_size, 0))

        for move in range(0, self.tile_size + 1):
            if direction == Position.DOWN:
                self.board.blit(background_tiles, (0, -move))
            elif direction == Position.UP:
                self.board.blit(background_tiles, (0, move - board_offset_y))
            elif direction == Position.RIGHT:
                self.board.blit(background_tiles, (-move, 0))
            elif direction == Position.LEFT:
                self.board.blit(background_tiles, (move - board_offset_x, 0))
            self.board.blit(player.image, (player_x, player_y))
            pygame.display.flip()

    def move_player(self, player, direction, tile_placements, tile_orientations, tiles):
        """
        Move player in direction specified, deciding whether to keep centred of freely move

        Parameters:
            player: Player
                player instance
            direction : int
                Direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            tile_placements : numpy.array(width, height)
                tile number at each position of the board
            tile_orientations : numpy.array(width, height)
                orientation of tile at each position on the board.
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
            tiles : TileSet.tiles
                Tiles in use
        """

        if (
            (direction == Position.LEFT or direction == Position.RIGHT)
            and self.centred_move_rect.collidepoint(
                player.position.x, self.total_mid_point.y
            )
            and self.centred_move_rect.collidepoint(
                player.position.get_next(direction).x, self.total_mid_point.y
            )
        ) or (
            (direction == Position.UP or direction == Position.DOWN)
            and self.centred_move_rect.collidepoint(
                self.total_mid_point.x, player.position.y
            )
            and self.centred_move_rect.collidepoint(
                self.total_mid_point.x, player.position.get_next(direction).y
            )
        ):
            self.move_player_centred(
                player, direction, tile_placements, tile_orientations, tiles
            )
            self.position_shift.move(direction)
        else:
            self.move_player_free(player, direction)


if __name__ == "__main__":
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

    # create board display
    x_tiles = 9
    y_tiles = 9

    x_tile_range = list(range(board_width))
    y_tile_range = list(range(board_height))
    rotation_range = list(range(-1, 2, 2))

    tile_size = tile_set.tiles[0].size
    plot = Plot(x_tiles, y_tiles, tile_size)

    # plot tiles
    position_shift = Position(4, 2)
    plot.show_all_tiles(
        board.tile_placements,
        board.tile_orientations,
        tile_set.tiles,
        position_shift=position_shift,
    )

    # wait for an exit
    while True:
        move = random.choice(
            ["left", "right", "up", "down", "rotate", "rotate", "rotate", "rotate"]
        )
        if move in ["left", "right", "up", "down"]:
            slide = move
            fill_tile_number = tile_bag.draw_tile()
            fill_tile_image = tile_set.tiles[fill_tile_number].image
            if slide == "left" or slide == "right":
                row_y = random.choice(y_tile_range)
                plot.slide_row(
                    row_y, slide, fill_tile_image, position_shift=position_shift
                )
            elif slide == "up" or slide == "down":
                column_x = random.choice(x_tile_range)
                plot.slide_column(
                    column_x, slide, fill_tile_image, position_shift=position_shift
                )
        elif move == "rotate":
            tile_position = Position(
                random.choice(x_tile_range), random.choice(y_tile_range)
            )
            rotation = random.choice(rotation_range)
            plot.rotate_tile(tile_position, rotation, position_shift=position_shift)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
