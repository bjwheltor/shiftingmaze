"""
Position

History
 24-Jul-2021 - Initial version separated from board.py
"""


class Position:
    """
    Represents a position as a set of coordinates

    Attributes
        x : int
            x-coordinate
        y : int
            y-coordinate
    """

    DIRECTIONS = [0, 1, 2, 3]
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

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

    def get_next(self, direction):
        """
        Get the position of the next point in a particular direction

        Parameters
            direction : int
                Direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right

        Returns
            next_position : Position
                position of next point as a set of coordinates
        """
        x = self.x
        y = self.y
        if direction == self.UP:
            y -= 1
        elif direction == self.LEFT:
            x -= 1
        elif direction == self.DOWN:
            y += 1
        elif direction == self.RIGHT:
            x += 1
        return Position(x, y)

    def move(self, direction):
        """
        Updates the position to the next point in a particular direction

        Parameters
            direction : int
                Direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right

        """
        if direction == self.UP:
            self.y -= 1
        elif direction == self.LEFT:
            self.x -= 1
        elif direction == self.DOWN:
            self.y += 1
        elif direction == self.RIGHT:
            self.x += 1

    def __repr__(self):
        """Display position"""
        return f"Position( x = {self.x}, y = {self.y} )"

    def __str__(self):
        """Print coordinates"""
        return f"x = {self.x}, y = {self.y}"


class Dimensions:
    """
    Represents the dimensions as a set of coordinates

    Attributes
        w : int
            width (x-coordinate)
        h : int
            height (y-coordinate)
    """

    def __init__(self, w, h):
        """
        Parameters
            w : int
                width (x-coordinate)
            h : int
                height (y-coordinate)
        """
        self.w = w
        self.h = h
        self.size = self.w * self.h

    def coords(self, rev=None):
        """
        Return position as a tuple

        Parameters
            none

        Keywords
            rev: bool
                true is dimension order to be reversed, i.e. (h, w) rather then (w, h)

        Returns
            coords : tuple
                dimensions as a tuple
        """
        if rev:
            coord = (self.h, self.xw)
        else:
            coords = (self.w, self.h)
        return coords

    def __repr__(self):
        """Display dimemsions"""
        return f"Dimensions( w = {self.w}, h = {self.h} )"

    def __str__(self):
        """Print dimemsions"""
        return f"w = {self.w}, h = {self.h}"
