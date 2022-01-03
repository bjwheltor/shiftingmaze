"""
View

History
29-Dec-2021 - Initial version - rationalisation of plot to separate concerns
"""


class View:
    """
    Represents the view of the section of the board that displayed

    Attributes:
        rect : pygame.Rect
            Rectangle describing view on board
        w : int
            Number of pixels in x-direction (left and right)
        h : int
            Number of pixels in y-direction (up and down)
    """

    def __init__(self, rect, placements, tileset):
        """
        Set-up view of board displaying tiles

        Parameters
            rect : pygame.Rect
                Rectangle describing view on board
            placements : numpy.array(h, w, n)
                holds all information on the state of the each square on the board.
                h is the y dimension
                w is the x dimension
                n is the board square attribute
            tiles : tiles.TileSet
                Details of the set of tiles being used
        """
        self.rect = rect
        self.board_colour = (0, 0, 0)  # BLACK
        self.tile_size = tile_set.tiles[0].size

        # create empty tile space
        self.empty_tile = pygame.Surface(
            (self.tile_size, self.tile_size), pygame.SRCALPHA
        )
        self.empty_tile.fill(self.board_colour)

        # display tiles
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                tile = tileset.get_image(placements[y, x, TILE], ROT)
                px, py = self.get_pxy(x, y)
                screen.blit(tile, (px, py))

        pygame.display.flip()

    def get_pxy(self, x, y):
        """
        Get pixel x, y position in view from board x, y position

        Parameters:
            x : int
                x position on board
            y : int
                y position on board
        Returns
            px : int
                pixel x position in view
            py : int
                pixel y position in view
        """
        px = (x - self.rect.left) * self.tile_size
        py = (y - self.rect.top) * self.tile_size
        return px, py

    def get_xy(self, px, py):
        """
        Get  board x, y position from pixel x, y position in view

        Parameters:
            px : int
                pixel x position in view
            py : int
                pixel y position in view

        Returns
            x : int
                x position on board
            y : int
                y position on board
        """
        x = int(px / self.tile_size + self.rect.left)
        y = int(py / self.tile_size + self.rect.top)
        return x, y

    def get_image(self, rect, add_tile=None, add_pxy=None):
        """
        Get image from screen (area from view)

        Parameters:
            px : int
                pixel x position in view
            py : int
                pixel y position in view
            pw : int
                width in pixels
            ph : int
                height in pixels
        Returns

        """
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(screen, (0, 0), rect)

        if add_tile:
            image.blit(add_tile, add_pxy)

        return image

    def rotate_tile(self, pos, rot):
        """
        Plot tile in position with orientation

        Parameters:
            pos : Position
                x, y coordinates of tile placement. (0, 0) = (left, top)
            rot : int
                rotation to be applied to tile. Either +1 or -1.
                +1 = 90 degrees anticlockwise. -1 = 90 degrees clockwise
        """
        print(f"Action: Rotate tile   rotation: {rot}")

        px, py = self.get_pxy(pos.x, pos.y)

        # extract tile from the board
        rect = pygame.Rect(px, py, self.tile_size, self.tile_size)
        tile = self.get_image(rect)
        tile_rect = tile.get_rect()

        # extract row to left of tile to be rotated
        rect = pygame.Rect(0, py, px + self.tile_size, self.tile_size)
        left_row = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(px, 0))

        # extract row to right of tile to be rotated
        rect = pygame.Rect(
            px, py, self.rect.width * self.tile_size - px, self.tile_size
        )
        right_row = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, 0))

        # extract column above tile to be rotated
        rect = pygame.Rect(px, 0, self.tile_size, py + self.tile_size)
        top_column = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, py))

        # extract column below tile to be rotated
        rect = pygame.Rect(
            px, py, self.tile_size, self.rect.height * self.tile_size - py
        )
        bottom_column = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, 0))

        for angle in range(0, rot * 91, rot):

            rotated_tile = pygame.transform.rotate(tile, angle)
            rotated_tile_rect = rotated_tile.get_rect()

            rotate_adjust_px = (rotated_tile_rect.right - tile_rect.right) // 2
            rotate_adjust_py = (rotated_tile_rect.bottom - tile_rect.bottom) // 2

            screen.blit(left_row, (-rotate_adjust_px, py))
            screen.blit(right_row, (px + rotate_adjust_px, py))
            screen.blit(top_column, (px, -rotate_adjust_py))
            screen.blit(bottom_column, (px, py + rotate_adjust_py))
            screen.blit(
                rotated_tile,
                (px - rotate_adjust_px, py - rotate_adjust_py),
            )

            pygame.display.flip()
            pygame.time.delay(10)

    def slide_tiles(self, x, y, dir):
        """
        Plot tile in position with orientation

        Parameters:
            x : int
                x position on board
            y : int
                x position on board
            dir : int
                direction in which to slide tiles
                0 = UP, 1 = LEFT, 2 = DOWN, 3 = RIGHT
        """
        print(f"Action: Slide tiles   direction: {dir}")

        px, py = self.get_pxy(x, y)

        # if slide to left
        if dir == 1:
            rect = pygame.Rect(
                0,
                py,
                (self.rect.width + 1) * self.tile_size,
                self.tile_size,
            )
            patch = self.get_image(
                rect,
                add_tile=self.empty_tile,
                add_pxy=(self.rect.width * self.tile_size, 0),
            )
        # if slide to right
        elif dir == 3:
            rect = pygame.Rect(
                -self.tile_size,
                py,
                (self.rect.width + 1) * self.tile_size,
                self.tile_size,
            )
            patch = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, 0))
        # if slide to up
        elif dir == 0:
            rect = pygame.Rect(
                px,
                0,
                self.tile_size,
                (self.rect.height + 1) * self.tile_size,
            )
            patch = self.get_image(
                rect,
                add_tile=self.empty_tile,
                add_pxy=(0, self.rect.height * self.tile_size),
            )
        # if slide to down
        elif dir == 2:
            rect = pygame.Rect(
                px,
                -self.tile_size,
                self.tile_size,
                (self.rect.height + 1) * self.tile_size,
            )
            patch = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, 0))

        # Slide the patch, overplotting the player if required
        for move in range(self.tile_size + 1):
            if dir == 1:
                screen.blit(patch, (-move, py))
            elif dir == 3:
                screen.blit(patch, (move - self.tile_size, py))
            elif dir == 0:
                screen.blit(patch, (px, -move))
            elif dir == 2:
                screen.blit(patch, (px, move - self.tile_size))

            pygame.display.flip()
            pygame.time.delay(10)

    def slide_line(self, dir, patch_rect, patch_placements, tileset):
        """
        Plot tile in position with orientation

        Parameters:
            x : int
                x position on board
            y : int
                x position on board
            dir : int
                direction in which to slide tiles
                0 = UP, 1 = LEFT, 2 = DOWN, 3 = RIGHT
        """
        print(f"Action: Slide tiles   direction: {dir}")

        px, py = self.get_pxy(patch_rect.left, patch_rect.top)

        # if slide to West
        if dir == WEST:
            px = 0
            dpx = (self.rect.width + 1) * self.tile_size
            dpy = self.tile_size
            x, _ = self.get_xy(dpx - self.tile_size, py)
            y = 0
            add_pxy = (self.rect.width * self.tile_size, 0)

            rect = pygame.Rect(px, py, dpx, dpy)
            tile = patch_placements[y, x, TILE]
            rot = patch_placements[y, x, ROT]
            add_tile = tileset.get_image(tile, rot)
            patch = self.get_image(rect, add_tile, add_pxy)

        # if slide to East
        elif dir == EAST:
            px = -self.tile_size
            dpx = (self.rect.width + 1) * self.tile_size
            dpy = self.tile_size
            x, _ = self.get_xy(px + self.tile_size, py)
            y = 0
            add_pxy = (0, 0)

            tile = patch_placements[y, x, TILE]
            rot = patch_placements[y, x, ROT]
            add_tile = tileset.get_image(tile, rot)
            rect = pygame.Rect(px, py, dpx, dpy)
            patch = self.get_image(rect, add_tile, add_pxy)

        # if slide to up
        elif dir == 0:
            rect = pygame.Rect(
                px,
                0,
                self.tile_size,
                (self.rect.height + 1) * self.tile_size,
            )
            patch = self.get_image(
                rect,
                add_tile=self.empty_tile,
                add_pxy=(0, self.rect.height * self.tile_size),
            )
        # if slide to down
        elif dir == 2:
            rect = pygame.Rect(
                px,
                -self.tile_size,
                self.tile_size,
                (self.rect.height + 1) * self.tile_size,
            )
            patch = self.get_image(rect, add_tile=self.empty_tile, add_pxy=(0, 0))

        # Slide the patch, overplotting the player if required
        for move in range(self.tile_size + 1):
            if dir == 1:
                screen.blit(patch, (-move, py))
            elif dir == 3:
                screen.blit(patch, (move - self.tile_size, py))
            elif dir == 0:
                screen.blit(patch, (px, -move))
            elif dir == 2:
                screen.blit(patch, (px, move - self.tile_size))

            pygame.display.flip()
            pygame.time.delay(10)


# ===============================
# Some tests in isolation
# ===============================
if __name__ == "__main__":
    print("SET UP FOR TESTING")
    # imports for testing and initialise
    import os
    import pygame
    import numpy as np

    from tile import *
    from tileset import *
    from tilebag import *
    from board import *

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
    tile_counts = {0: 40, 1: 140, 2: 80, 3: 80, 4: 20}

    tile_set = TileSet(doors_for_tiles, tile_counts, name=tileset_name)
    tile_bag = TileBag(tile_set)

    # Set up dimensions of board and view
    board_width = 5
    board_height = board_width
    view_width = 3
    view_height = view_width
    view_left = (board_width - view_width) // 2
    view_top = (board_height - view_height) // 2
    view_rect = pygame.Rect(view_left, view_top, view_width, view_height)

    # Create board and fill with tiles from tile bag
    board = Board(board_width, board_height, tile_bag=tile_bag)

    # Set up screen display
    SCREEN_X_ORIGIN = 0
    SCREEN_Y_ORIGIN = 0
    SCREEN_WIDTH = view_width * tile_set.tiles[0].size
    SCREEN_HEIGHT = view_height * tile_set.tiles[0].size
    os.environ["SDL_VIDEO_WINDOW_POS"] = (
        str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
    )
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Shifting Maze")

    print("START TESTING")
    print("Test 1: Set-up view in screen")
    view = View(view_rect, board.placements, tile_set)
    pygame.time.delay(1000)

    print("Test 2: Rotation of tiles")
    pos = Position(3, 3)
    rot = 1
    view.rotate_tile(pos, rot)
    pygame.time.delay(1000)

    rot = -1
    view.rotate_tile(pos, rot)
    pygame.time.delay(1000)

    print("Test 3: Slide lines of tiles")
    dir = EAST
    x_or_y = 3
    print(board)
    patch_rect, patch_placements = board.slide_line(dir, x_or_y, tile_bag)
    view.slide_line(dir, patch_rect, patch_placements, tile_set)
    print(board)
    pygame.time.delay(1000)

    dir = WEST
    x_or_y = 3
    print(board)
    patch_rect, patch_placements = board.slide_line(dir, x_or_y, tile_bag)
    view.slide_line(dir, patch_rect, patch_placements, tile_set)
    print(board)
    pygame.time.delay(100000)

    dir = 0
    view.slide_tiles(x, y, dir)
    pygame.time.delay(1000)

    dir = 2
    view.slide_tiles(x, y, dir)

    pygame.time.delay(5000)
