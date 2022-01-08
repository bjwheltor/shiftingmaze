"""
History
17-Jul-2021: Initial version-controlled code for tile generation and management. 
    Note: walls now changes to access with opposite truth values.
30-Dec-2021: Split TileBag off into separate module
08-Jan-2022: Added return_tiles method and tests
"""
import random
import pygame


class TileBag:
    """
    Represents the bag of tiles from which random ones can be drawn for the Shifting Maze game.

    Attributes
        tile_numbers : list
            List of the tiles in the bag in a random order
    """

    def __init__(self, tile_set):
        """
        Parameters
            tile_set : TileSet
                Set of tiles in play for a game of the Shifting Maze.
        """
        self.tile_numbers = []
        for tile_number, tile_count in tile_set.tile_counts.items():
            self.tile_numbers += [tile_number] * tile_count
        self.mix()

    def mix(self):
        """Mix the content of the bag"""
        random.shuffle(self.tile_numbers)

    def draw_tile(self):
        """
        Draw a single tile from the bag

        Parameters
            none

        Returns
            tile_number : int
                Number of tile drawn
        """
        return self.tile_numbers.pop()

    def draw_tiles(self, number=1):
        """
        Draw a number tiles from the bag

        Parameters
            number : int
                Number of tiles to be drawn. Default = 1

        Returns
            tile_list : list
                List of the tiles
        """
        tile_list = []
        for n in range(number):
            tile_list.append(self.draw_tile())
        return tile_list

    def return_tile(self, tile_number):
        """
        Return a single tile to the bag and shuffle

        Parameters
            tile_number : int
                Number of tile drawn
        """
        self.tile_numbers.append(tile_number)
        self.mix()

    def return_tiles(self, tile_list):
        """
        Return a tiles to the bag and shuffle

        Parameters
            tile_list : list
                List of the tiles
        """
        self.tile_numbers += tile_list
        self.mix()

    def __repr__(self):
        """Display tile bag"""
        tile_list = ""
        for tile_number in self.tile_numbers:
            tile_list += str(tile_number) + " "
        return tile_list

    def __str__(self):
        """Print tile bag"""
        tile_list = ""
        for tile_number in self.tile_numbers:
            tile_list += str(tile_number) + " "
        return f"Tile bag: {tile_list}"


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
    tile_counts = {0: 2, 1: 2, 2: 2, 3: 2, 4: 2}

    tile_set = TileSet(doors_for_tiles, tile_counts, name=tileset_name)

    tile_bag = TileBag(tile_set)

    print("START TESTING")
    print("Test 1: Print tile bag")
    print(tile_bag)
    print("Test 2: Draw a tile")
    tile = tile_bag.draw_tile()
    print(f"Tile drawn: {tile}")
    print(tile_bag)
    print("Test 3: Draw 3 tiles")
    tiles = tile_bag.draw_tiles(3)
    print(f"Tiles drawn: {tiles}")
    print(tile_bag)
    print("Test 4: Return tile")
    print(f"Tile to be returned: {tile}")
    tile_bag.return_tile(tile)
    print(tile_bag)
    print("Test 5: Return 3 tiles")
    print(f"Tiles to be returned: {tiles}")
    tile_bag.return_tiles(tiles)
    print(tile_bag)
