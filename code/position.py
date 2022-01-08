"""
Represents a position as a set of coordinates

History

24-Jul-2021: Initial version separated from board.py

02-Jan-2022: Moved direction constants to separate module
    and removed Dimensions class
"""
from direction import *


class Position:
    """
    Represents a position as a set of coordinates

    Attributes
        x : int
            x-coordinate
        y : int
            y-coordinate
    """

    def __init__(self, x, y):
        """
        Parameters
            x : int
                x-coordinate
            y : int
                y-coordinate
        """
        self.x = x
        self.y = y

    def coords(self, rev=None):
        """
        Return position as a tuple

        Parameters
            none

        keywords
            rev: bool
                true is coordinate order to be reversed, i.e. (y, x) rather then (x, y)

        Returns
            xy : tuple
                position as a tuple
        """
        if rev:
            coords = (self.y, self.x)
        else:
            coords = (self.x, self.y)
        return coords

    def get_next(self, dir):
        """
        Get the position of the next point in a particular direction

        Parameters
            dir : int
                Direction in which position to be returned
                0 = NORTH, 1 = WEST, 2 = SOUTH, 3 = EAST

        Returns
            next_position : Position
                position of next point as a set of coordinates
        """
        x = self.x
        y = self.y
        if direction == NORTH:
            y -= 1
        elif direction == WEST:
            x -= 1
        elif direction == SOUTH:
            y += 1
        elif direction == EAST:
            x += 1
        return Position(x, y)

    def move(self, direction):
        """
        Updates the position to the next point in a particular direction

        Parameters
            dir : int
                Direction in which position to be returned
                0 = NORTH, 1 = WEST, 2 = SOUTH, 3 = EAST

        """
        if direction == NORTH:
            self.y -= 1
        elif direction == WEST:
            self.x -= 1
        elif direction == SOUTH:
            self.y += 1
        elif direction == EAST:
            self.x += 1

    def __repr__(self):
        """Display position"""
        return f"Position( x = {self.x}, y = {self.y} )"

    def __str__(self):
        """Print coordinates"""
        return f"x = {self.x}, y = {self.y}"
