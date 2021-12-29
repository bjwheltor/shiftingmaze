Board
=====

This class holds the current configuration of the rooms (called tiles) in the maze. 

Placements
----------

All the relevant information is held in a single
NumPy array called ``placements``, set-up as follows::

    placements : numpy.array(h, w, n)

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

Tile manipulation
-----------------

The Board class has a number of methods to manipulate tiles within the placements array:

 * ``place_tile`` - sets tile number and orientation at a given position
 * ``rotate_tile`` - updates the orientation of a tile at a given position
   by applying a rotation
 * ``slide_row`` - slides a row of tiles 1 place to the left or right, 
   filling in from the tile bag, returning a patch one longer than the row
   with all the tile numbers and orientations
 * ``slide_col`` - slides a row of tiles 1 place to the left or right, 
   filling in from the tile bag, returning a patch one longer than the row
   with all the tile numbers and orientations

Door checks
-----------

The Board class also has a method for checking for a door:
 * ``check_for_door``

By default this checks the tile at the given position looking in the 
specified direction, but if ``next = True``, it checks from the next tile
in the specificed direction looking back towards the given position.
This is because to move to an adjacent tile you need doors to exist on 
both the current tile and the one you are moving to.

Special
-------

There is a further method:

 * ``get_patch``- returns a patch (area of tiles),
   given a ``Rect`` for the area,
   drawing new tiles from tile bag is required.

.. note:: It is not clear whether this method is still required.
  