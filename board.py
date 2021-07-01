"""
Board
History

 - v1 - Initial version
"""
import numpy as np


class Board:
    """
    Represents the state of the board for Shifting Maze game.

    Attributes:
        width : int
            dimension of board in x direction (left and right)
        height : list
            dimension of board in y direction (up and down)
        tile_placements : numpy.array(width, height)
            Tile number at each position of the board
        tile_orientations : numpy.array(width, height)
            Orientation of tile at each position on the board.
            0 = no rotation, 1 = 90 degrees rotation anticlockwise
            2 = 180 degrees rotation, 3 = 90 degrees rotation clockwise
    """

    def __init__(self, width=10, height=10, setup="visible"):
        """
        Parameters:
        width : int
            dimension of board in x direction (left and right). Default = 10
        height : list
            dimension of board in y direction (up and down). Default = 10
        """
        self.width = width
        self.height = height
        self.tile_placements = np.empty([self.width, self.height], dtype=int)
        self.tile_orientations = np.array([self.width, self.height], dtype=int)

    def place_tile(self, tile_x, tile_y, tile_number, tile_orientation=0):
        """
        Place a tile onto the board.
        Set the position to the tile number and the orientation.

        Parameters:
            tile_x
                x-coordinate of tile placement. Left = 0
            tile_y
                y-coordinate of tile placement. Top = 0
            tile_number : int
                Number of tile to be placed
            tile_orientation : int
                Orientation of tile to be placed
        """
        self.tile_placements[tile_x, tile_y] = tile_number
        self.tile_orientations[tile_x, tile_y] = tile_orientation

    def rotate_tile(self, tile_x, tile_y, rotation):
        """
        Rotate a tile on the board. Reset the orientation.

        Parameters:
            tile_x
                x-coordinate of tile placement. Left = 0
            tile_y
                y-coordinate of tile placement. Top = 0
            rotation : int
                rotation to be applied to tile.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        tile_orientation = self.tile_orientations[tile_x, tile_y]
        self.tile_orientations[tile_x, tile_y] = (tile_orientation + rotation) % 4

    def check_for_door(self, tile_x, tile_y, direction, tiles):
        """
        Check if exit exists in a particular direction from a tile on the board

        Parameters:
            tile_x
                x-coordinate of tile placement. Left = 0
            tile_y
                y-coordinate of tile placement. Top = 0
            direction : int
                Direction in which presence of door to be checked.
                0 = up, 1 = left, 2 = down, 3 = right
            tiles : TileSet.tiles
                Tiles in use
        """
        tile_number = self.tile_placements[tile_x, tile_y]
        doors = tiles[tile_number].doors
        tile_orientation = self.tile_orientations[tile_x, tile_y]
        door_index = (direction - tile_orientation) % 4
        return doors[door_index]

    def access_in_direction(self, x, y, direction):
        """
        Checks if movement out of off current tile is possible and whether movement into neighbouring
        tile (or edge) is possible and returns two logicals, clear and clear_next respectively, if it is
        """
        new_x, new_y = new_xy_from_direction(x, y, direction)

        current_clear = self.check_for_wall(x, y, direction)

        if current_clear:
            if (
                new_x < 0
                or new_x > self.board_width - 1
                or new_y < 0
                or new_y > self.board_height - 1
            ):
                new_clear = False
            else:
                reverse_direction = (direction + 2) % 4
                new_clear = self.check_for_wall(new_x, new_y, reverse_direction)
        else:
            new_clear = False

        return current_clear, new_clear

    def slide_row(self, row_y, slide=1):
        """ """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.board_width + abs_slide, dtype=int)
        if slide > 0:
            extended_placements[abs_slide:] = self.tile_placements[:, row_y]
            self.tile_placements[:, row_y] = extended_placements[: self.board_width]
        else:
            extended_placements[: self.board_width] = self.tile_placements[:, row_y]
            self.tile_placements[:, row_y] = extended_placements[abs_slide:]

    def slide_column(self, column_x, slide=1):
        """ """
        abs_slide = abs(slide)
        extended_placements = np.zeros(self.board_height + abs_slide, dtype=int)
        if slide > 0:
            # update board positions
            extended_placements[abs_slide:] = self.tile_placements[column_x, :]
            self.tile_placements[column_x, :] = extended_placements[: self.board_height]
        else:
            extended_placements[: self.board_height] = self.tile_placements[column_x, :]
            self.tile_placements[column_x, :] = extended_placements[abs_slide:]


if __name__ == "__main__":
    board = Board
