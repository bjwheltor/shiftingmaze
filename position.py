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

    def coords(self):
        """
        Return position as a tuple

        Parameters
            none

        Returns
            xy : tuple
                position as a tuple
        """
        return (self.x, self.y)

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


if __name__ == "__main__":
    # test position
    print(f"Position.UP = {Position.UP}")
    print(f"Position.UP = {Position.LEFT}")
    print(f"Position.UP = {Position.DOWN}")
    print(f"Position.UP = {Position.RIGHT}")
