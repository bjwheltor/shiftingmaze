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
    """

    def __init__(self, number, name, colour, pos, floor_colour):
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
            self.background, floor_colour, self.rect
        )  # TODO: correct to set correct colour and use later
