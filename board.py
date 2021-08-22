"""
Board

History
17-Jul-2021 - Initial version
24-Jul-2021 - Position class moved into a separate file
"""
import os
import sys
import random
import pygame
import numpy as np

from tiles import *
from position import *


class Board:
    """
    Represents the state of the board for Shifting Maze game.

    Attributes:
        width : int
            dimension of board in x direction (left and right)
        height : list
            dimension of board in y direction (up and down)
        tile_placements : numpy.array(width, height)
            tile number at each position of the board
        tile_orientations : numpy.array(width, height)
            orientation of tile at each position on the board.
            0 = no rotation, 1 = 90 degrees rotation anticlockwise
            2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
    """

    def __init__(self, width=10, height=10, tile_bag=None):
        """
        Parameters:
        width : int
            dimension of board in x direction (left and right). Default = 10
        height : list
            dimension of board in y direction (up and down). Default = 10
        """
        self.width = width
        self.height = height
        self.size = self.width * self.height

        if tile_bag:
            self.tile_placements = np.array(tile_bag.draw_tiles(self.size), dtype=int)
            self.tile_orientations = np.array(
                random.choices([0, 1, 2, 3], k=self.size), dtype=int
            )
            self.tile_placements.shape = (self.width, self.height)
            self.tile_orientations.shape = (self.width, self.height)
        else:
            self.tile_placements = np.empty([self.width, self.height], dtype=int)
            self.tile_orientations = np.array([self.width, self.height], dtype=int)

    def place_tile(self, position, tile_number, tile_orientation=0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Parameters:
            position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
            tile_number : int
                Number of tile to be placed
            tile_orientation : int
                Orientation of tile to be placed
        """
        self.tile_placements[position.coords()] = tile_number
        self.tile_orientations[position.coords()] = tile_orientation

    def rotate_tile(self, position, rotation):
        """
        Rotate a tile on the board. Reset the orientation.

        Parameters:
            position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
            rotation : int
                rotation to be applied to tile.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        tile_orientation = self.tile_orientations[position.coords()]
        self.tile_orientations[position.coords()] = (tile_orientation + rotation) % 4

    def check_for_door(self, position, direction, tiles, next=None):
        """
        Check if exit exists in a particular direction from a tile on the board

        Parameters:
            position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
            direction : int
                Direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            tiles : TileSet.tiles
                Tiles in use

        Keywords:
            next : logical
                If true check for door coming from next tile

        Returns
            door : logical
                True if door is present, False if not
        """
        if next:
            check_position = position.get_next(direction)
            check_direction = (direction + 2) % 4
        else:
            check_position = position
            check_direction = direction
        tile_number = self.tile_placements[check_position.coords()]
        tile_orientation = self.tile_orientations[check_position.coords()]
        doors = tiles[tile_number].doors
        door_index = (check_direction - tile_orientation) % 4
        return doors[door_index]

    def slide_row(self, row_y, slide=1):
        """
        Slide a row a number of tiles along

        Parameters:
            row_y : int
                y-coordinate of row

        Keywords:
            slide : int
                How many places to slide (-ve = left, +ve = right). Default = 1
        """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.board_width + abs_slide, dtype=int)
        if slide > 0:
            extended_placements[abs_slide:] = self.tile_placements[:, row_y]
            self.tile_placements[:, row_y] = extended_placements[: self.width]
        else:
            extended_placements[: self.board_width] = self.tile_placements[:, row_y]
            self.tile_placements[:, row_y] = extended_placements[abs_slide:]

    def slide_column(self, column_x, slide=1):
        """
        Slide a column number of tiles along

        Parameters:
            column_x : int
                x-coordinate of column

        Keywords:
            slide : int
                How many places to slide (-ve = left, +ve = right). Default = 1
        """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.height + abs_slide, dtype=int)
        if slide > 0:
            # update board positions
            extended_placements[abs_slide:] = self.tile_placements[column_x, :]
            self.tile_placements[column_x, :] = extended_placements[: self.board_height]
        else:
            extended_placements[: self.board_height] = self.tile_placements[column_x, :]
            self.tile_placements[column_x, :] = extended_placements[abs_slide:]


if __name__ == "__main__":
    # screen set-up to test
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    DARK_GREY = (64, 64, 64)
    LIGHT_GREY = (192, 192, 192)
    BLACK = (0, 0, 0)
    BLUE = (150, 150, 255)
    YELLOW = (200, 200, 0)
    RED = (200, 100, 100)
    GREEN = (100, 200, 100)

    SCREEN_X_ORIGIN = 0
    SCREEN_Y_ORIGIN = 0
    SCREEN_WIDTH = 1020
    SCREEN_HEIGHT = 1020

    os.environ["SDL_VIDEO_WINDOW_POS"] = (
        str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
    )
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill(WHITE)
    pygame.display.flip()

    # Create a tileset
    doors_for_tiles = {
        0: [1, 1, 1, 1],
        1: [0, 1, 1, 1],
        2: [0, 0, 1, 1],
        3: [0, 1, 0, 1],
        4: [0, 0, 0, 1],
    }
    tile_counts = {0: 20, 1: 70, 2: 40, 3: 40, 4: 10}
    tile_set = TileSet(doors_for_tiles, tile_counts, name="standard")
    tile_bag = TileBag(tile_set)

    print(tile_bag.tile_numbers)
    print()

    # Create board and fill with tiles from tile bag
    board = Board(width=10, height=10, tile_bag=tile_bag)

    print(tile_bag.tile_numbers)

    # display board
    for x in range(board.width):
        for y in range(board.height):
            tile_number = board.tile_placements[x, y]
            screen.blit(tile_set.tiles[tile_number].image, (x * 102, y * 102))
    pygame.display.flip()

    # wait for an exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
