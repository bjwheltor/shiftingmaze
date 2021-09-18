"""
Board

History
17-Jul-2021 - Initial version
24-Jul-2021 - Position class moved into a separate file
21-Aug-2021 - Simplified variables and naming - more use of Position and Dimensions, 
              noted as pos and dim variables
14-Sep-2021 - Separation of concerns - updated to focus board on key functionality,
              including placements and orientations into a single array to simplify
              passing of information and allow for future extension
"""
import random
import numpy as np

from tiles import *
from position import *


class Board:
    """
    Represents the state of the board for Shifting Maze game.

    Attributes:
        dim : Dimension
            (x, y) dimensions of board in tiles: (width (w), height (h))
        w : int
            x-dimension of board in tiles in x direction (left and right): width
        h : int
            y-dimension of board in tiles y direction (up and down): height
        n : int
            number of board quare attributes
        size : int
            total number of tiles on board (w * h)
        placements : numpy.array(h, w, n)
            holds all information on the state of the each square on the board.
            h is the y dimension
            w is the x dimension
            n is the board square attribute:
                TILE = 0 is the tile number
                ROT = 1 is the rotation or orientation of each tile,
                0 = no rotation, 1 = 90 degrees rotation anticlockwise
                2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
    """

    TILE = 0
    ROT = 1

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
        self.n = 2

        self.placements = np.empty([self.h, self.w, self.n], dtype=int)

        if tile_bag:
            tiles = np.array(tile_bag.draw_tiles(self.size), dtype=int)
            rots = np.array(random.choices(Position.DIRECTIONS, k=self.size), dtype=int)
            tiles.shape = (self.h, self.w)
            rots.shape = (self.h, self.w)
        elif tile_list:
            tiles = np.array(tile_list, dtype=int)
            tiles.shape = (self.h, self.w)
            rots = np.zeros((self.h, self.w), dtype=int)

        self.placements[:, :, Board.TILE] = tiles
        self.placements[:, :, Board.ROT] = rots

    def place_tile(self, pos, tile, rot=0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            tile : int
                number of tile to be placed
            rot : int
                rotation of tile to be placed
        """
        self.placements[pos.y, pos.x, Board.TILE] = tile
        self.placements[pos.y, pos.x, Board.ROT] = rot

    def rotate_tile(self, pos, rotate):
        """
        Rotate a tile on the board. Reset the orientation.

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            rotate : int
                rotate tile: +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        rot = self.placements[pos.y, pos.x, Board.ROT]
        self.placements[pos.y, pos.x, Board.ROT] = (rot + rotate) % 4

    def check_for_door(self, pos, dir, tiles, next=False):
        """
        Check if exit exists in a particular direction from a tile on the board

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            dir : int
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
            pos_to_check = pos.get_next(dir)
            dir_to_check = (dir + 2) % 4
        else:
            pos_to_check = pos
            dir_to_check = dir
        tile = self.placements[pos_to_check.y, pos_to_check.x, Board.TILE]
        rot = self.placements[pos_to_check.y, pos_to_check.x, Board.ROT]
        doors = tiles[tile].doors
        door_index = (dir_to_check - rot) % 4
        return doors[door_index]

    def slide_row(self, row, dir, tile_bag):
        """
        Slide column nup or down 1 tile

        Parameters:
            row : int
                (full) board y (tile) coordinate of row
            dir : int
                Direction in column to be slid
                0 = up, 2 = down
            tile_bag : TileBag
                bag of tiles from which random ones can be drawn

        Returns
            patch_placements : numpy.array(h, w, n)
                holds all information on the state of the each square on the board.in the 'patch'
        """
        patch_placements = np.empty([1, self.w + 1, self.n], dtype=int)
        if dir == Position.LEFT:
            patch_placements[0, : self.w, :] = self.placements[row, ...]
            patch_placements[0, self.w, Board.TILE] = tile_bag.draw_tile()
            patch_placements[0, self.w, Board.ROT] = random.choice(Position.DIRECTIONS)
            self.placements[row, ...] = patch_placements[0, 1:, :]
            tile_bag.return_tile(patch_placements[0, 0, Board.TILE])
        elif dir == Position.RIGHT:
            patch_placements[0, 1:, :] = self.placements[row, ...]
            patch_placements[0, 0, Board.TILE] = tile_bag.draw_tile()
            patch_placements[0, 0, Board.ROT] = random.choice(Position.DIRECTIONS)
            self.placements[row, ...] = patch_placements[0, : self.w, :]
            tile_bag.return_tile(patch_placements[0, self.w, Board.TILE])
        return patch_placements

    def slide_col(self, col, dir, tile_bag):
        """
        Slide column nup or down 1 tile

        Parameters:
            col : int
                (full) board x (tile) coordinate of column
            dir : int
                Direction in column to be slid
                0 = up, 2 = down
            tile_bag : TileBag
                bag of tiles from which random ones can be drawn

        Returns
            patch_placements : numpy.array(h, w, n)
                holds all information on the state of the each square on the board.in the 'patch'
        """
        patch_placements = np.empty([self.h + 1, 1, self.n], dtype=int)
        if dir == Position.UP:
            patch_placements[: self.h, 0, :] = self.placements[:, col, :]
            patch_placements[self.h, 0, Board.TILE] = tile_bag.draw_tile()
            patch_placements[self.h, 0, Board.ROT] = random.choice(Position.DIRECTIONS)
            self.placements[:, col, :] = patch_placements[1:, 0, :]
            tile_bag.return_tile(patch_placements[0, 0, Board.TILE])
        elif dir == Position.DOWN:
            patch_placements[1:, 0, :] = self.placements[:, col, :]
            patch_placements[0, 0, Board.TILE] = tile_bag.draw_tile()
            patch_placements[0, 0, Board.ROT] = random.choice(Position.DIRECTIONS)
            self.placements[:, col, :] = patch_placements[: self.h, 0, :]
            tile_bag.return_tile(patch_placements[self.h, 0, Board.TILE])
        return patch_placements

    def __str__(self):
        """Print board details"""
        string = f"Board layout: {self.w} x {self.h} tiles\n"

        header1 = "Tiles" + " " * max(0, (self.w - len("Tiles")))
        header2 = "Rotations" + " " * max(0, (self.w - len("Rotations")))
        string += header1 + " " + header2 + "\n"
        for y in range(self.h):
            tiles_row = ""
            rots_row = ""
            for x in range(self.w):
                tiles_row += str(self.placements[y, x, Board.TILE])
                rots_row += str(self.placements[y, x, Board.ROT])
            string += f"{tiles_row} {rots_row}\n"
        return string


#
# Some tests in isolation
#
if __name__ == "__main__":
    # extra imports for testing and initialise
    from player import *
    from text import *

    print("START TESTING")

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
    print("Create Board")
    board_dim = Dimensions(5, 5)
    board = Board(board_dim, tile_list=tile_list)
    print(board)

    # Place tile
    pos = Position(1, 1)
    tile = 4
    rot = 3
    print("Place Tile")
    print(f"pos: {pos}  tile: {tile}  rot: {rot}")
    board.place_tile(pos, tile, rot=rot)
    print(board)

    # Test rotate tile
    rotate = -1
    print("Rotate Tile")
    print(f"pos: {pos}  rot: {rot}")
    board.rotate_tile(pos, rotate=rotate)
    print(board)

    # Check for slide row
    row = 1
    dir = Position.RIGHT
    print("\nSlide row")
    print(f"row: {row}  dir: {dir}")
    patch = board.slide_row(row, dir, tile_bag)
    print(board)
    print(f"\npatch: {patch}")

    # Check for slide column
    col = 1
    dir = Position.UP
    print("\nSlide column")
    print(f"col: {col}  dir: {dir}")
    patch = board.slide_col(col, dir, tile_bag)
    print(board)
    print(f"\npatch: {patch}")

    # Check for door
    print(tile_set)
    dir = Position.UP
    print("Check for door")
    print(f"pos: {pos}  dir: {dir}")
    print(f"tile: {board.placements[pos.y,pos.x, Board.TILE]}")
    door = board.check_for_door(pos, dir, tile_set.tiles)
    print(f"door is {door}")

    # Check for door in next tile
    dir = Position.UP
    print("\nCheck for door in next tile")
    print(f"pos: {pos}  dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set.tiles, next=True)
    print(f"door is {door}")

    print()
    print(board.placements.shape)
    print(board.placements.ndim)
    print(board.placements.shape[0])
    print(board.placements.shape[1])
    print(board.placements.shape[2])
