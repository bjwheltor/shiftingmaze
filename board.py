"""
Board

History
17-Jul-2021 - Initial version
24-Jul-2021 - Position class moved into a separate file
21-Aug-2021 - Simplified variables and naming - more use of Position and Dimensions, 
              noted as pos and dim variables
"""
import random
import numpy as np

from tiles import *
from position import *


class Board:
    """
    Represents the state of the board for Shifting Maze game.

    Attributes:
        dim : Postion
            (x, y) dimensions of board in tiles: (width (w), height (h))
        w : int
            x-dimension of board in tiles in x direction (left and right): width
        h : int
            y-dimension of board in tiles y direction (up and down): height
        size : int
            total number of tiles on board (w * h)
        placements : numpy.array(h, w)
            tile number at each position of the board - ordering (y, x)
        orientations : numpy.array(h, w)
            orientation of tile at each position on the board - ordering (y, x)
            0 = no rotation, 1 = 90 degrees rotation anticlockwise
            2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
    """

    def __init__(self, dim, tile_bag=None, tile_list=None):
        """
        Create board of specified size and fill with tiles drawn randomly from the tile bag
        and assigned random orientations.

        Parameters:
        dim : Position
            (x, y) dimensions of board in tiles: (width (w), height (h))

        Keywords:
            tile_bag : TileBag
                represents the bag of tiles from dimich random ones can be drawn.
                Default is None, dimich sets empty placement and orientation arrays
        """
        self.dim = dim
        self.w = self.dim.w
        self.h = self.dim.h
        self.size = self.w * self.h

        if tile_bag:
            self.placements = np.array(tile_bag.draw_tiles(self.size), dtype=int)
            self.orientations = np.array(
                random.choices(Position.DIRECTIONS, k=self.size), dtype=int
            )
            self.placements.shape = (self.h, self.w)
            self.orientations.shape = (self.h, self.w)
        elif tile_list:
            self.placements = np.array(tile_list, dtype=int)
            self.placements.shape = (self.h, self.w)
            self.orientations = np.zeros((self.h, self.w), dtype=int)
        else:
            self.placements = np.empty([self.h, self.w], dtype=int)
            self.orientations = np.array([self.h, self.w], dtype=int)

    def place_tile(self, pos, tile, orientation=0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            tile : int
                number of tile to be placed
            orientation : int
                orientation of tile to be placed
        """
        self.placements[pos.coords(rev=True)] = tile
        self.orientations[pos.coords(rev=True)] = orientation

    def rotate_tile(self, pos, rotation):
        """
        Rotate a tile on the board. Reset the orientation.

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            rotation : int
                rotation to be applied to tile.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        orientation = self.orientations[pos.coords(rev=True)]
        self.orientations[pos.coords(rev=True)] = (orientation + rotation) % 4

    def check_for_door(self, pos, direction, tiles, next=None):
        """
        Check if exit exists in a particular direction from a tile on the board

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
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
            pos_to_check = pos.get_next(direction)
            direction_to_check = (direction + 2) % 4
        else:
            pos_to_check = pos
            direction_to_check = direction
        tile = self.placements[pos_to_check.coords(rev=True)]
        orientation = self.orientations[pos_to_check.coords(rev=True)]
        doors = tiles[tile].doors
        door_index = (direction_to_check - orientation) % 4
        return doors[door_index]

    def apply_patch(self, pos, patch_placements, patch_orientations):
        """
        Apply a patch (new set of values) to a section of the placements and orientations

        Parameters:
            pos : Position
                (full) board x, y (tile) coordinates of top left of where patch to be applied
        patch_placements : numpy.array
            tile number at each position of the board - ordering (y, x)
        orientations : numpy.array
            orientation of tile at each position on the board - ordering (y, x)
            0 = no rotation, 1 = 90 degrees rotation anticlockwise
            2 = 180 degrees rotation, 3 = 90 degrees rotation clockwis
        """
        h, w = patch_placements.shape
        x, y = pos.coords()
        x_end = x + w
        y_end = y + h
        self.placements[y:y_end, x:x_end] = patch_placements[:, :]
        self.orientations[y:y_end, x:x_end] = patch_orientations[:, :]

    def __str__(self):
        """Print board details"""
        string = f"Board layout: {self.w} x {self.h} tiles\n"
        header1 = "Placements" + " " * max(0, (self.w - len("Placements")))
        header2 = "Orientations" + " " * max(0, (self.w - len("Orientations")))
        string += header1 + " " + header2 + "\n"
        for y in range(self.h):
            placements_row = ""
            orientations_row = ""
            for x in range(self.w):
                placements_row += str(self.placements[y, x])
                orientations_row += str(self.orientations[y, x])
            string += f"{placements_row} {orientations_row}\n"
        return string


#
# Some tests in isolation
#
if __name__ == "__main__":
    # extra imports for testing and initialise
    from player import *
    from text import *

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

    #
    # Start Testing
    # print tile set and board set-up for reference
    print()
    print(tile_set)
    print(board)

    # test apply patch
    pos = Position(1, 0)
    patch_placements = np.array([[5], [6], [7], [8], [9]], dtype=int)
    patch_orientations = np.array([[1], [1], [1], [1], [1]], dtype=int)

    print()
    print(patch_placements)
    print(patch_orientations)
    board.apply_patch(pos, patch_placements, patch_orientations)

    print()
    print(board)
