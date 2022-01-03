"""
TileBag

History

17-Jul-2021 - Initial version-controlled code for tile generation and management. 
    Note: walls now changes to access with opposite truth values.
30-Dec-2021 - Split TileBag off into separate module
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
        return tile_list


#
# Some tests in isolation
#
if __name__ == "__main__":
    # extra imports for testing
    import os
    import sys

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

    # display tiles
    x = 0
    y = 0
    count = 0
    for tile_number in tile_bag.tile_numbers:
        if count < 100:
            screen.blit(tile_set.tiles[tile_number].image, (x * 102, y * 102))
        x = x + 1
        if x == 10:
            y = y + 1
            x = 0
    pygame.display.flip()

    print(tile_bag.tile_numbers)
    print()
    print(tile_bag.draw_tiles(3))
    print()
    print(tile_bag.tile_numbers)
    print()
    print(tile_bag.draw_tiles())
    print()
    print(tile_bag.tile_numbers)
    print()
    print(tile_bag.draw_tile())
    print()
    print(tile_bag.tile_numbers)

    # wait for an exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
