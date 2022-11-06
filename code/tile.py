import pygame


class Tile:
    """
    Represents a tile including image of tile.

    Attributes:
        number (int):
            Unique number assigned to tile.
        doors (list):
            List of values representing no door or blank wall (0) or a door (1).
            These proceed clockwise from up the screen. Has default value.
        size (int):
            Length of one edge of a square tile, including frame. Default: 102.
        frame (int):
            Width of frame around edge of tile. Default: 1.
        wall_width (int):
            Thickness of walls. Default: 10.
        door_width (int):
            Width of doorways. Default: 50.
        image (pygame.Surface)
            Image of tile.
        rect (pygame.Rect):
            Rectangle describing tile image.
        frame_colour (tuple):
            Red, green, blue tuple for colour of frame around tile.
            Default: (192, 192, 192) = LIGHT_GREY.
        wall_colour (tuple):
            Red, green, blue tuple for colour of walls.
            Default: (200, 100, 100) = RED.
        floor_colour (tuple):
            Red, green, blue tuple for colour of floor.
            Default: (150, 150, 255) = BLUE.
    """

    def __init__(self, number: int, doors: list = [1, 1, 1, 1]):
        """
        Args:
            number:
                Unique number assigned to tile

        Keyword Args:
                List of values representing no door or blank wall (0) or a door (1).
                These proceed anti-clockwise from up the screen, with default value.
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
            self.right_door_rect = (
                self.size - self.wall_width - self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.right_door_rect)

        if doors[2]:
            self.bottom_door_rect = (
                int((self.size - self.door_width) / 2),
                self.size - self.wall_width - self.frame,
                self.door_width,
                self.wall_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.bottom_door_rect)

        if doors[3]:
            self.left_door_rect = (
                self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.left_door_rect)
