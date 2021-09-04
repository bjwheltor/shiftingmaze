"""
Provide text output as game info and for debugging

History
30-Aug-2021 - Initial version
"""


class Text:
    """
    Provide text output as game info and for debugging for Shifting Maze game.

    Attributes:
    """

    def __init__(self):
        """ """
        pass

    def player_state(self, player, plot, board, tile_set):
        """ """
        pos = player.pos.coords(rev=True)
        placement = board.placements[pos]
        orientation = board.orientations[pos]
        doors = tile_set.tiles[placement].doors

        print(f"Player pos: {pos}    Plot shift pos: {plot.shift_pos}")
        print(f"Board tile: {placement} {doors}   orientation: {orientation}\n")
