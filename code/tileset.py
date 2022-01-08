"""
History
17-Jul-2021: Initial version-controlled code for tile generation and management. 
    Note: walls now changes to access with opposite truth values.
30-Dec-2021: Split TileSet off into separate module
08-Jan-2022: Added tests and better exit condition using utilities
"""
import utilities
from tile import *


class TileSet:
    """
    Represents a set of tiles for use in the Shifting Maze game.

    Attributes
        name : string
            Name of tile set. Default: "standard".
        tiles : dict
            Dictionary of tiles indexed by the tile number.
        tile_counts : int
            Number of each tile in set.
    """

    def __init__(self, doors_for_tiles, tile_counts, name="standard"):
        """
        Parameters
            name : string
                Name of tile set. Default: "standard"
            doors_for_tiles : dict
                Dictionary with lists of doors for each tile.
                Each list represents no door or blank wall (0) or a door (1) for each side.
                These proceed anti-clockwise from up the screen.
            tile_counts : dict
                Dictionary with then number of each tile in set.
        """
        self.name = name
        self.tile_counts = tile_counts
        self.different_tiles = len(tile_counts)
        self.tiles = {}
        for tile_number, doors in doors_for_tiles.items():
            self.tiles[tile_number] = Tile(tile_number, doors)

    def get_image(self, number, rot=None):
        if rot is None:
            rot = 0
        image = self.tiles[number].image
        rotated_image = pygame.transform.rotate(image, -rot)
        return rotated_image

    def __str__(self):
        """Print set of tiles"""
        string = f"Tile set: {self.name}\n"
        for number in range(self.different_tiles):
            string += f" {number}:{self.tiles[number].doors}\n"
        return string


# ===============================
# Some tests in isolation
# ===============================
if __name__ == "__main__":
    print("SET UP FOR TESTING")
    # imports for testing and initialise
    import os
    import sys
    import pygame

    from direction import *
    from tile import *
    from tileset import *

    # Initiate pygame
    pygame.init()

    # Create a tile set and fill tile bag
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

    view_width = 5
    view_height = 5

    # Set up screen display
    SCREEN_X_ORIGIN = 0
    SCREEN_Y_ORIGIN = 0
    SCREEN_WIDTH = view_width * tile_set.tiles[0].size
    SCREEN_HEIGHT = view_height * tile_set.tiles[0].size
    os.environ["SDL_VIDEO_WINDOW_POS"] = (
        str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
    )
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Shifting Maze Tile Set")

    print("START TESTING")
    print("Test 1: Print tile set")
    print(tile_set)
    print("Test 2: Display tile set with no rotation")
    tile_size = tile_set.tiles[0].size
    for tile_number in range(tile_set.different_tiles):
        tile = tile_set.tiles[tile_number].image
        px = tile_number * tile_size
        screen.blit(tile, (px, 0))
        pygame.display.flip()

    print("Test 3: Display tile set with all rotations (starting with 0)")
    for y in range(4):
        py = (y + 1) * tile_size
        rotation = DIRECTIONS[y]
        for tile_number in range(tile_set.different_tiles):
            tile = tile_set.get_image(tile_number, rotation)
            px = tile_number * tile_size
            screen.blit(tile, (px, py))
            pygame.display.flip()

    # wait for an exit
    utilities.wait_for_exit()
