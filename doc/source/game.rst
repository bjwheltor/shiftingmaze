Game
====

The main module is game.py, which handles all the main set up 
and holds the game loop.

Set-up
------

Imports
^^^^^^^

External imports::

    import sys
    import pygame
    import numpy as np

Internal imports::

    from position import *
    from tiles import *
    from player import *
    from board import *
    from plot import *
    from text import *

Initialisation
^^^^^^^^^^^^^^

Pygame is initialised with::

    pygame.init()

Constants
^^^^^^^^^

A number of top level constants are defined.

Colours::
    
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    DARK_GREY = (64, 64, 64)
    LIGHT_GREY = (192, 192, 192)
    BLACK = (0, 0, 0)
    BLUE = (150, 150, 255)
    YELLOW = (200, 200, 0)
    RED = (200, 100, 100)
    GREEN = (100, 200, 100)

Input keys::

    MOVE_KEYS = (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)
    ROTATE_KEYS = (pygame.K_z, pygame.K_x)
    SLIDE_ROW_KEYS = (pygame.K_q, pygame.K_w)
    SLIDE_COLUMN_KEYS = (pygame.K_p, pygame.K_l)

Random events
^^^^^^^^^^^^^

A pygame random event identifier is declared
and set to trigger every 3 seconds in the game loop::

    RANDOM = pygame.USEREVENT + 0
    pygame.time.set_timer(RANDOM, 3000)

Tile set
^^^^^^^^

The code allows the creation of a simple tile set for debugging the game
or the standard (full) tile sset for actually playing the game::

    test_tileset = False

    if test_tileset:
        tileset_name = "test"
        doors_for_tiles = {
            0: [1, 1, 1, 1],
        }
        tile_counts = {0: 300}
    else:
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
    tile_size = tile_set.tiles[0].size

The details are explained under the Tiles section.

Board
^^^^^

The full dimensions of the board are set using the Dimensions class,
and used to create a board from Tiles in the TileBag::

    board_dim = Dimensions(7, 7)
    board = Board(board_dim, tile_bag=tile_bag)

.. note:: The dimensions of the board most be an odd number
    to allow for the centring of the player on the display.


Display
^^^^^^^

The dimensions of the viewable section of the board are set 
using the Dimensions class, 
as well as the offset between the full and viewable board
and the display is created, using Plot::

    view_dim = Dimensions(5, 5)
    shift_pos = Position((board.w - view_dim.w) // 2, (board.h - view_dim.h) // 2)
    plot = Plot(view_dim, board.placements, tile_set.tiles, shift_pos=shift_pos)

Player
^^^^^^

The player position is set to be the centre of the board, 
with other player attributes being set 
before the player is created::

    player_pos = Position(shift_pos.x + (view_dim.w // 2), shift_pos.y + (view_dim.h // 2))
    player_name = "Bruce"
    player_number = 1
    player_colour = GREEN
    start_tile = tile_set.tiles[0]

    player = Player(player_name, player_number, player_colour, player_pos, start_tile)
    plot.show_player(player)

Text
^^^^

Set-up a text output object
(mainly for ease of providing diagnostic output to the screen)
and print some initial information::

    text = Text()
    print()
    print(tile_set)
    print(board)
    print("Game Start")
    text.player_state(player, plot, board, tile_set)

.. warning:: The use of diagnostic text output has not between
    implemented consistently yet.

Loop
----

The game loop in just a simple while loop, with a logical, starting::

    running = True
    
    while running:

        pygame.display.update()

The final statement here updates the whole display window,
which might not actually be necessary at this point, 
given the Plot set-up also this, and the changes in the game
loop tend to also have updates.

Event handling
^^^^^^^^^^^^^^

All the events are returned in ``event`` and handled in a loop::

    for event in pygame.event.get():

The game can be exited by quitting (selecting "x" on the window)
or by selecting the escape key::

    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False

Four further keys allow a direction of movement to be selected, 
with the current tile occupied by the player
and it's orientation being stored::

    elif event.key in MOVE_KEYS:

        tile = tile_set.tiles[
            board.placements[player.pos.y, player.pos.x, Board.TILE]
        ]
        rot = board.placements[player.pos.y, player.pos.x, Board.ROT]

        if event.key == pygame.K_UP:
            dir = Position.UP
        elif event.key == pygame.K_LEFT:
            dir = Position.LEFT
        elif event.key == pygame.K_DOWN:
            dir = Position.DOWN
        elif event.key == pygame.K_RIGHT:
            dir = Position.RIGHT

These selections then lead to a number of outcomes, not discussed here.

Two more key allow rotatation of the current tile occupied by the player
to be selected, either anticlockwise or clockwise::

    elif event.key in ROTATE_KEYS:
        if event.key == pygame.K_z:
            rotation = 1
        elif event.key == pygame.K_x:
            rotation = -1
            plot.rotate_tile(player.pos, rotation)
            board.rotate_tile(player.pos, rotation)  

Again, these selections then lead to a number of outcomes, not discussed here.

The last type of event is random (i.e. not initiated by the player),
which may lead to further random choices::

    elif event.type == RANDOM:
        random_event = random.choice([0])
        if random_event == 0:
            dir = random.choice(Position.DIRECTIONS)
            if dir == Position.RIGHT or dir == Position.LEFT:
                row = random.choice(range(board.w))

In this example, the choice is to slide a row or column,
with the second cloice determining the direction
and the third choice determining which row (in this case).

.. note:: At present the only random event implemented is to 
    slide a row or column.

Exit
----

Once the game loop is exited by setting ``running = False``,
a clean exit is handled with::

    pygame.quit()
    sys.exit()


    pygame.display.update()