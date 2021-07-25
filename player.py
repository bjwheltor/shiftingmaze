"""
Player
History

 - v1 - Initial version
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
        position : Position
            x,y coordinates of tile placement. (0, 0) = (left, top)
    """

    def __init__(self, number, name, colour, position):
        """
        Create player and place player

        Parameters:
            number: int
                unique identifying number of play
            name: str
                name of player
            colour: RGB colour tuple
                colour of player image
            position : Position
                x,y coordinates of tile placement. (0, 0) = (left, top)
        """
        self.number = number
        self.name = name
        self.colour = colour
        self.position = position
        self.size = 40
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, self.colour, self.rect)
        self.background = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(self.background, self.colour, self.rect)


if __name__ == "__main__":
    print(f"Position.UP = {Position.UP}")
    print(f"Position.UP = {Position.LEFT}")
    print(f"Position.UP = {Position.DOWN}")
    print(f"Position.UP = {Position.RIGHT}")

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
    SCREEN_WIDTH = 100
    SCREEN_HEIGHT = 100

    MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
    ROTATE_KEYS = (pygame.K_z, pygame.K_x)
    SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
    SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)

    os.environ["SDL_VIDEO_WINDOW_POS"] = (
        str(SCREEN_X_ORIGIN) + "," + str(SCREEN_Y_ORIGIN)
    )
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill(WHITE)
    pygame.display.flip()

    # test position of player
    player_name = "Bruce"
    player_number = 1
    player_colour = GREEN
    player_position = Position(0, 0)
    player = Player(player_name, player_number, player_colour, player_position)
    print(f"Position: {player.position}")

    # Game loop
    running = True
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in MOVE_KEYS:
                    if event.key == pygame.K_UP:
                        direction = Position.UP
                    elif event.key == pygame.K_LEFT:
                        direction = Position.LEFT
                    elif event.key == pygame.K_DOWN:
                        direction = Position.DOWN
                    elif event.key == pygame.K_RIGHT:
                        direction = Position.RIGHT
                player.position.move(direction)
                print(f"Position: {player.position}")
