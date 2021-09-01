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
                random.choices([0, 1, 2, 3], k=self.size), dtype=int
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
                Direction in dimich presence of door to be checked.
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

    def slide_row(self, row, slide=1):
        """
        Slide a row a number of tiles along

        Parameters:
            row : int
                y-coordinate of row

        Keywords:
            slide : int
                How many places to slide (-ve = left, +ve = right). Default = 1
        """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.w + abs_slide, dtype=int)
        if slide > 0:
            extended_placements[abs_slide:] = self.placements[row, :]
            self.placements[row, :] = extended_placements[: self.w]
        else:
            extended_placements[: self.w] = self.placements[row, :]
            self.placements[row, :] = extended_placements[abs_slide:]

    def slide_column(self, col, slide=1):
        """
        Slide a column number of tiles along

        Parameters:
            col : int
                x-coordinate of column

        Keywords:
            slide : int
                How many places to slide (-ve = left, +ve = right). Default = 1
        """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.h + abs_slide, dtype=int)
        if slide > 0:
            # update board positions
            extended_placements[abs_slide:] = self.placements[:, col]
            self.placements[:, col] = extended_placements[: self.h]
        else:
            extended_placements[: self.h] = self.placements[:, col]
            self.placements[:, col] = extended_placements[abs_slide:]

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
