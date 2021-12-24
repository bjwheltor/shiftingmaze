"""
Player
History

 17-Jul-2021 - Initial version
 21-Aug-2021 - Simplified variables and naming - more use of Position, noted as pos variables
"""
import pygame
from board import *
from position import *


class Player:
    """
    A class to represent a player, with visual characteristics

    Attributes:
        number: int
            unique identifying number of play
        name: str
            name of player
        image: pygame.Surface
            image of player avatar
        rect: pygame.Rect
            rectangle for player image
        pos : Position
            x, y coordinates of tile placement. (0, 0) = (left, top)
        floor_colour : tuple
            Red, green, blue tuple for colour of floor.
        player_offset : Position
            x,y coordinates of player offset from top left of tile in plot space. Default: Position(20,20)
    """

    DO_NOT_MOVE = 0
    MOVE_WITH_TILES = 1
    STAY_AS_TILES_MOVE = 2

    def __init__(self, number, name, colour, pos, tile):
        """
        Create player and place player

        Parameters:
            number: int
                unique identifying number of play
            name: str
                name of player
            colour: RGB colour tuple
                colour of player image
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
        """
        self.number = number
        self.name = name
        self.colour = colour
        self.pos = pos
        self.size = 40
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, self.colour, self.rect)

        self.background = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(
            self.background, tile.floor_colour, self.rect
        )  # TODO: correct to set correct colour and use later
        self.offset = Position(
            int((tile.size - self.rect.w) / 2),
            int((tile.size - self.rect.h) / 2),
        )
