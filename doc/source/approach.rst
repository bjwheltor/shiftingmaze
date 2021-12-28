Approach
========

The code is written in a way that attempt sto maintain separation of concerns.
The main concerns, separated in to classes, being:

 * State of the board (Board)
 * Display of the action though a viewing window onto the board (Plot)
 * Properties of the tile (Tile)
 * A get of tiles used for game play (TileSet)
 * A bag of tiles used for game play (TileBag)
 * Properties of a player, including position (Player)

.. note:: This separation is not as clean as it should be at present.