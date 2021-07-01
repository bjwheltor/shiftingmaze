"""
Tiles
History

 - v1 - Initial version-controlled code for tile generation and management. 
 Note: walls now changes to access with opposite truth values.
"""
import os
import sys
import random
import pygame


class Tile:
    """
    Represents a tile in the Shifting Maze game, including image of tile.

    Attributes:
        number : int
            Unique number assigned to tile
        doors : list
            List of values representing no door or blank wall (0) or a door (1).
            These proceed anti-clockwise from up the screen. Default: [1,1,1,1]
        size : integer
            Length of one edge of a square tile, including frame. Default: 102
        frame : int
            Width of frame around edge of tile. Default: 1
        wall_width : int
            Thickness of walls. Default: 10
        door_width : int
            Width of doorways. Default: 50
        image : pygame.Surface
            Image of tile
        rect : pygame.Surface.rect
            Rectangle describing tile image
        frame_colour : tuple
            Red, green, blue tuple for colour of frame around tile.
            Default: (192, 192, 192) = LIGHT_GREY
        wall_colour : tuple
            Red, green, blue tuple for colour of walls
            Default: (200, 100, 100) = RED
        floor_colour : tuple
            Red, green, blue tuple for colour of floor.
            Default: (150, 150, 255) # BLUE
    """

    def __init__(self, number, doors=[1, 1, 1, 1]):
        """
        Parameters:
            number : int
                Unique number assigned to tile
            doors : list
                List of values representing no door or blank wall (0) or a door (1).
                These proceed anti-clockwise from up the screen. Default: [1,1,1,1]
        """
        self.number = number
        self.doors = doors

        self.size = 102
        self.frame = 1
        self.wall_width = 10
        self.door_width = 50

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        self.frame_colour = (192, 192, 192)  # LIGHT_GREY
        self.rect = self.image.get_rect()
        self.image.fill(self.frame_colour)

        self.wall_colour = (200, 100, 100)  # RED
        self.full_rect = (
            self.frame,
            self.frame,
            self.size - 2 * self.frame,
            self.size - 2 * self.frame,
        )
        pygame.draw.rect(self.image, self.wall_colour, self.full_rect)

        self.floor_colour = (150, 150, 255)  # BLUE
        self.floor_rect = (
            self.frame + self.wall_width,
            self.frame + self.wall_width,
            self.size - 2 * (self.frame + self.wall_width),
            self.size - 2 * (self.frame + self.wall_width),
        )
        pygame.draw.rect(self.image, self.floor_colour, self.floor_rect)

        if doors[0]:
            self.top_door_rect = (
                int((self.size - self.door_width) / 2),
                self.frame,
                self.door_width,
                self.wall_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.top_door_rect)

        if doors[1]:
            self.left_door_rect = (
                self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.left_door_rect)

        if doors[2]:
            self.bottom_door_rect = (
                int((self.size - self.door_width) / 2),
                self.size - self.wall_width - self.frame,
                self.door_width,
                self.wall_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.bottom_door_rect)

        if doors[3]:
            self.right_door_rect = (
                self.size - self.wall_width - self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.right_door_rect)


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
        self.tiles = {}
        for tile_number, doors in doors_for_tiles.items():
            self.tiles[tile_number] = Tile(tile_number, doors)
        random.shuffle(self.tiles)


class TileBag:
    """
    Represents the bag of tilesfrom which random ones can be drawn for the Shifting Maze game.

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
        """Draw a single tile from the bag

        Parameters
            number : int
                Number of tiles to be drawn. Default = 1

        Returns
            tile_number : int
                Number of tile drawn
        """
        return self.tile_numbers.pop()

    def draw_tiles(self, number=1):
        """Draw a number tiles from the bag

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
