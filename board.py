"""
Board

History
17-Jul-2021 - Initial version
24-Jul-2021 - Position class moved into a separate file
21-Aug-2021 - Simplified variables and naming - more use of Position, noted as xy variables
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
        wh : Postion
            (x, y) dimensions of board in tiles: (width (w), height (h))
        w : int
            x-dimension of board in tiles in x direction (left and right): width
        h : int
            y-dimension of board in tiles y direction (up and down): height
        size : int
            total number of tiles on board (w * h)
        placements : numpy.array(w, h)
            tile number at each position of the board
        orientations : numpy.array(w, h)
            orientation of tile at each position on the board.
            0 = no rotation, 1 = 90 degrees rotation anticlockwise
            2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
    """

    def __init__(self, wh, tile_bag=None):
        """
        Create board of specified size and fill with tiles drawn randomly from the tile bag
        and assigned random orientations.

        Parameters:
        wh : Position
            (x, y) dimensions of board in tiles: (width (w), height (h))

        Keywords:
            tile_bag : TileBag
                represents the bag of tiles from which random ones can be drawn.
                Default is None, which sets empty placement and orientation arrays
        """
        self.wh = wh
        self.w = self.wh.x
        self.h = self.wh.y
        self.size = self.w * self.h

        if tile_bag:
            self.placements = np.array(tile_bag.draw_tiles(self.size), dtype=int)
            self.orientations = np.array(
                random.choices([0, 1, 2, 3], k=self.size), dtype=int
            )
            self.placements.shape = (self.w, self.h)
            self.orientations.shape = (self.w, self.h)
        else:
            self.placements = np.empty([self.w, self.h], dtype=int)
            self.orientations = np.array([self.w, self.h], dtype=int)

    def place_tile(self, xy, tile, orientation=0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Parameters:
            xy : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            tile : int
                number of tile to be placed
            orientation : int
                orientation of tile to be placed
        """
        self.placements[xy.coords()] = tile
        self.orientations[xy.coords()] = orientation

    def rotate_tile(self, xy, rotation):
        """
        Rotate a tile on the board. Reset the orientation.

        Parameters:
            xy : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            rotation : int
                rotation to be applied to tile.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        orientation = self.orientations[xy.coords()]
        self.orientations[xy.coords()] = (orientation + rotation) % 4

    def check_for_door(self, xy, direction, tiles, next=None):
        """
        Check if exit exists in a particular direction from a tile on the board

        Parameters:
            xy : Position
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
            xy_to_check = xy.get_next(direction)
            direction_to_check = (direction + 2) % 4
        else:
            xy_to_check = xy
            direction_to_check = direction
        tile = self.placements[xy_to_check.coords()]
        orientation = self.orientations[xy_to_check.coords()]
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
            extended_placements[abs_slide:] = self.placements[:, row]
            self.placements[:, row] = extended_placements[: self.w]
        else:
            extended_placements[: self.w] = self.placements[:, row]
            self.placements[:, row] = extended_placements[abs_slide:]

    def slide_column(self, column, slide=1):
        """
        Slide a column number of tiles along

        Parameters:
            column : int
                x-coordinate of column

        Keywords:
            slide : int
                How many places to slide (-ve = left, +ve = right). Default = 1
        """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.h + abs_slide, dtype=int)
        if slide > 0:
            # update board positions
            extended_placements[abs_slide:] = self.placements[column, :]
            self.placements[column, :] = extended_placements[: self.h]
        else:
            extended_placements[: self.h] = self.placements[column, :]
            self.placements[column, :] = extended_placements[abs_slide:]
