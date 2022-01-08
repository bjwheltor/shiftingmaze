"""
Provide text output as game info and for debugging for Shifting Maze game

History

30-Aug-2021: Initial version
"""
from board import *


class Text:
    """
    Provide text output as game info and for debugging

    Attributes:
    """

    def __init__(self):
        """ """
        pass

    def player_state(self, player, plot, board, tile_set):
        """ """
        tiles = board.placements[player.pos.x, player.pos.y, Board.TILE]
        rots = board.placements[player.pos.x, player.pos.y, Board.ROT]
        doors = tile_set.tiles[tiles].doors

        print(f"Player pos: {player.pos}    Plot shift pos: {plot.shift_pos}")
        print(f"Board tile: {tiles} {doors}   orientation: {rots}\n")
