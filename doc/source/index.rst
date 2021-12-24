.. shiftingmaze documentation master file, created by
   sphinx-quickstart on Thu Dec 23 14:43:35 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Shifting Maze Documentation
===========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Introduction
------------

Shifting Maze is a graphical game where the player attempts to navigate a 
finite, 2D array of rooms, each having between 0 and 3 walls (or between 1 
and 4 doorways). As well as moving between the rooms through the doorways, 
the player can also rotate the current room they are in, opening up new
possiblities for navigation through the 'maze'. The configuration of the
'maze' of rooms changes as rooms rotate and rows and columns slide randomly.

To allow the number of rooms to be large, only a subset of the rooms are 
displayed, centred on the player, so as the player moves through the maze
the rooms appear to move with the player remaining at the centre of the 
viewing window.

Classes
-------

Board
^^^^^

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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
