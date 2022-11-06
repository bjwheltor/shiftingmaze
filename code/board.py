import pygame
import random
import numpy as np

from typing import Tuple

from position import *
from direction import *

from tileset import *
from tilebag import *

NATTR = 2
TILE = 0
ROT = 1


class Board:
    """
    Represents the state of the board.
    This is initialised either by drawing a set of tiles from a Tile Bag and
    assigning random orientations for by specifying an explicit list of tiles.

    Attributes:
        width (int):
            X-dimension of board in tiles in x direction (west and east)
        height (int):
            Y-dimension of board in tiles y direction (north and south)
        nattr (int):
            Number of board square attributes (NATT), where the attributes are
            TILE (0) is the tile number
            ROT (1) is the rotation or orientation of each tile (degrees clockwise)
        size (int):
            Total number of tiles on board (w * h)
        placements (numpy.ndarray):
            Holds all information on the state of the each square
            on the board. Has dimensions h, w, n
    """

    def __init__(
        self, width: int, height: int, tile_bag: TileBag = None, tile_list: list = None
    ):
        """
        Create board of specified size and fill with tiles drawn randomly from the tile bag
        and assigned random orientations.

        Args:
            width:
                X-dimension of board in tiles in x direction (west and east)
            height:
                Y-dimension of board in tiles y direction (north and south)

        Keyword Args:
            tile_bag:
                Represents the bag of tiles from dimich random ones can be drawn.
                Default is None, which sets empty placement and orientation arrays
            tile_list:
                List of tile numbers
        """
        self.width = width
        self.height = height
        self.nattr = NATTR
        self.size = self.width * self.height

        # Currently maintained to stop code breaking
        self.w = self.width
        self.h = self.height
        self.n = self.nattr

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.placements = np.empty([self.height, self.width, self.nattr], dtype=int)

        if tile_bag:
            tiles = np.array(tile_bag.draw_tiles(self.size), dtype=int)
            rots = np.array(random.choices(DIRECTIONS, k=self.size), dtype=int)
            tiles.shape = (self.height, self.width)
            rots.shape = (self.height, self.width)
        elif tile_list:
            tiles = np.array(tile_list, dtype=int)
            tiles.shape = (self.height, self.width)
            rots = np.zeros((self.height, self.width), dtype=int)

        self.placements[:, :, TILE] = tiles
        self.placements[:, :, ROT] = rots

    def place_tile(self, pos: Position, tile: int, rot: int = 0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Args:
            pos:
                X, y coordinates of tile placement. (0, 0) = (west, north)
            tile:
                Number of tile to be placed

        Keyword Args:
            rot:
                Orientation of tile to be placed (rotation degrees clockwise)
        """
        self.placements[pos.y, pos.x, TILE] = tile
        self.placements[pos.y, pos.x, ROT] = rot

    def rotate_tile(self, pos: Position, rotate: int):
        """
        Rotate a tile on the board. Reset the orientation.

        Args:
            pos:
                X, y coordinates of tile placement. (0, 0) = (west, north)
            rotate:
                Rotatation to be applied to tile (degrees clockwise)
        """
        rot = self.placements[pos.y, pos.x, ROT]
        self.placements[pos.y, pos.x, ROT] = (rot + rotate) % FULLCIRCLE

    def slide_line(
        self, dir: int, x_or_y: int, tile_bag: TileBag = None
    ) -> Tuple[pygame.Rect, np.ndarray]:
        """
        Slide a row or column

        Args:
            dir:
                Direction in which to slide tiles
            x_or_y:
                X or y position on board, depending on direction.
                For dir = NORTH or SOUTH, this is x, indicating the column.
                For dir = EAST or WEST, this is y, indicating the row.
            tilebag:
                Bag of tiles from which new one can be drawn

        Returns:
            - Rectangle of tiles to slide, including new tile
            - Holds all information on the state of the each square on the board
              in the 'patch' (this will be either a row or column and one longer
              than the board, e.g. for a raw (1, w+1, n)
        """
        if dir == WEST:
            patch_rect = pygame.Rect(0, x_or_y, self.w + 1, 1)
            patch_placements = np.empty([1, self.w + 1, self.n], dtype=int)
            patch_placements[0, : self.w, :] = self.placements[x_or_y, ...]
            patch_placements[0, self.w, TILE] = tile_bag.draw_tile()
            patch_placements[0, self.w, ROT] = random.choice(DIRECTIONS)
            self.placements[x_or_y, ...] = patch_placements[0, 1:, :]
            tile_bag.return_tile(patch_placements[0, 0, TILE])
        elif dir == EAST:
            patch_rect = pygame.Rect(-1, x_or_y, self.w + 1, 1)
            patch_placements = np.empty([1, self.w + 1, self.n], dtype=int)
            patch_placements[0, 1:, :] = self.placements[x_or_y, ...]
            patch_placements[0, 0, TILE] = tile_bag.draw_tile()
            patch_placements[0, 0, ROT] = random.choice(DIRECTIONS)
            self.placements[x_or_y, ...] = patch_placements[0, : self.w, :]
            tile_bag.return_tile(patch_placements[0, self.w, TILE])
        if dir == NORTH:
            patch_rect = pygame.Rect(x_or_y, 0, 1, self.h + 1)
            patch_placements = np.empty([self.h + 1, 1, self.n], dtype=int)
            patch_placements[: self.h, 0, :] = self.placements[:, x_or_y, :]
            patch_placements[self.h, 0, TILE] = tile_bag.draw_tile()
            patch_placements[self.h, 0, ROT] = random.choice(DIRECTIONS)
            self.placements[:, x_or_y, :] = patch_placements[1:, 0, :]
            tile_bag.return_tile(patch_placements[0, 0, TILE])
        elif dir == SOUTH:
            patch_rect = pygame.Rect(x_or_y, -1, 1, self.h + 1)
            patch_placements = np.empty([self.h + 1, 1, self.n], dtype=int)
            patch_placements[1:, 0, :] = self.placements[:, x_or_y, :]
            patch_placements[0, 0, TILE] = tile_bag.draw_tile()
            patch_placements[0, 0, ROT] = random.choice(DIRECTIONS)
            self.placements[:, x_or_y, :] = patch_placements[: self.h, 0, :]
            tile_bag.return_tile(patch_placements[self.h, 0, TILE])

        return patch_rect, patch_placements

    def check_for_door(
        self, pos: int, dir: int, tile_set: TileSet, next: bool = False
    ) -> bool:
        """
        Check if exit exists in a particular direction from a tile on the board.

        Args:
            pos:
                X, y coordinates of tile placement. (0, 0) = (left, top)
            dir:
                Direction in which presence of door to be checked.
            tile_set:
                Set of tiles in use.

        Keyword Args:
            next:
                If true check for door coming from next tile

        Returns:
            True if door is present, False if not
        """
        if next:
            pos_to_check = pos.get_next(dir)
            dir_to_check = (dir + PLUS180) % FULLCIRCLE
        else:
            pos_to_check = pos
            dir_to_check = dir
        tile = self.placements[pos_to_check.y, pos_to_check.x, TILE]
        rot = self.placements[pos_to_check.y, pos_to_check.x, ROT]
        doors = tile_set.tiles[tile].doors
        door_index = int(((dir_to_check - rot) % FULLCIRCLE) / PLUS90)
        return doors[door_index]

    def __str__(self) -> str:
        """Print board details"""
        string = f"Board layout: {self.w} x {self.h} tiles\n"
        string += "Tiles/Rotations\n"
        for y in range(self.h):
            for x in range(self.w):
                if y == 0:
                    if x == 0:
                        header = "y \\ x "
                    header += f"  {x:2d}    "
                    if x == self.w - 1:
                        string += header + "\n"
                if x == 0:
                    row = f"{y:2d}   "
                row += f"{self.placements[y, x, TILE]:2d} {self.placements[y, x, ROT]:3d}  "
                if x == self.w - 1:
                    string += row + "\n"
        return string


# ===============================
# Some tests in isolation
# ===============================
if __name__ == "__main__":
    print("SET UP FOR TESTING")
    print("Imports for testing and initialise")
    import os
    import pygame
    import numpy as np

    from tile import *
    from tileset import *
    from tilebag import *

    print("Initiate pygame")
    pygame.init()

    print("Create a tile set and fill tile bag")
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

    print("Set up dimensions of board and view")
    board_width = 7
    board_height = board_width
    view_width = 5
    view_height = view_width
    view_left = (board_width - view_width) // 2
    view_top = (board_height - view_height) // 2
    view_rect = pygame.Rect(view_left, view_top, view_width, view_height)

    print("\nSTART TESTING")
    print("Test 1: Set-up Board")
    board = Board(board_width, board_height, tile_bag=tile_bag)
    print(board)

    print("Test 2: Place tile")
    pos = Position(1, 1)
    tile = 1
    rot = PLUS0
    print(f"pos: {pos}  tile: {tile}  rot: {rot}")
    board.place_tile(pos, tile, rot=rot)
    print(board)

    print("Test 3: Rotate tile")
    rotate = PLUS90
    print(f"pos: {pos}  rot: {rot}")
    board.rotate_tile(pos, rotate=rotate)
    print(board)

    print("Test 4: Slide row")
    dir = EAST
    x_or_y = 1
    print(f"x_or_y: {x_or_y}  dir: {dir}")
    placement_rect, placement_patch = board.slide_line(dir, x_or_y, tile_bag)
    print(f"placement_rect: {placement_rect}")
    print(f"placement_patch:\n{placement_patch}")
    print(board)

    dir = WEST
    print(f"x_or_y: {x_or_y}  dir: {dir}")
    placement_rect, placement_patch = board.slide_line(dir, x_or_y, tile_bag)
    print(f"placement_rect: {placement_rect}")
    print(f"placement_patch:\n{placement_patch}")
    print(board)

    print("Test 5: Slide column")
    x_or_y = 1
    dir = NORTH
    print(f"x_or_y: {x_or_y}  dir: {dir}")
    placement_rect, placement_patch = board.slide_line(dir, x_or_y, tile_bag)
    print(f"placement_rect: {placement_rect}")
    print(f"placement_patch:\n{placement_patch}")
    print(board)

    dir = SOUTH
    print(f"x_or_y: {x_or_y}  dir: {dir}")
    placement_rect, placement_patch = board.slide_line(dir, x_or_y, tile_bag)
    print(f"placement_rect: {placement_rect}")
    print(f"placement_patch:\n{placement_patch}")
    print(board)

    print("Test 6: Check for doors")
    print(tile_set)
    print(
        f"tile: {board.placements[pos.y, pos.x, TILE]} {board.placements[pos.y, pos.x, ROT]}  pos: {pos}"
    )
    dir = NORTH
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"door is {door}")
    dir = EAST
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"door is {door}")
    dir = SOUTH
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"door is {door}")
    dir = WEST
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"door is {door}")

    print("Test 7: Check for doors in next tile")
    print(tile_set)
    print(
        f"tile: {board.placements[pos.y, pos.x, TILE]} {board.placements[pos.y, pos.x, ROT]}  pos: {pos}"
    )
    dir = NORTH
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"check for door in next tile")
    print(f"pos: {pos.get_next(dir)}")
    door = board.check_for_door(pos, dir, tile_set, next=True)
    print(f"door is {door}")
    dir = EAST
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"check for door in next tile")
    print(f"pos: {pos.get_next(dir)}")
    door = board.check_for_door(pos, dir, tile_set, next=True)
    print(f"door is {door}")
    dir = SOUTH
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"check for door in next tile")
    print(f"pos: {pos.get_next(dir)}")
    door = board.check_for_door(pos, dir, tile_set, next=True)
    print(f"door is {door}")
    dir = WEST
    print(f"dir: {dir}")
    door = board.check_for_door(pos, dir, tile_set)
    print(f"check for door in next tile")
    print(f"pos: {pos.get_next(dir)}")
    door = board.check_for_door(pos, dir, tile_set, next=True)
    print(f"door is {door}")
