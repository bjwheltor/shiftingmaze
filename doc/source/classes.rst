Classes
=======

Board
-----

This holds the current configuration of the rooms (called tiles) 
in the maze. All the relevant information is held in a single
NumPy array called ``placements``, set-up as follows:

    ``placements : numpy.array(h, w, n)``

where:
 * ``h`` (height) is the y-dimension of board in tiles y direction (up and down)
 * ``w`` (width) is the x-dimension of board in tiles in x direction (left and right)
 * ``n`` is the number of board square attributes

``h`` and ``w`` are actually held as an ``Dimension`` object, ``dim``, 
with ``size = w * h`` being the  total number of tiles on board 
        
There are two board square attribute (``n = 2``):
 * ``TILE = 0`` is the tile number
 * ``ROT = 1`` is the rotation or orientation of each tile, which takes the values:

   * ``0`` = no rotation
   * ``1`` = 90 degrees rotation anticlockwise
   * ``2`` = 180 degrees rotation
   * ``3`` = 90 degrees rotation clockwise