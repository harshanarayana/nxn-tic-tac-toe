from utils.contracts import require


class Player(object):
    """Provide a Player Representation for the Tic-Tac-Toe Game"""

    @require("Player name has to be a String value",
             lambda args: isinstance(args.name, str))
    @require("Player Marker can be one of X/O",
             lambda args: args.marker.lower() in ["x", "o"])
    def __init__(self, name: str, marker: str):
        """
        Initialize a new Player with name and assigned Marker.
        :param name: Player Name
        :param marker: Player Identification (X/O)
        """
        self._name: str = name
        self._marker: str = marker

    @property
    def marker(self) -> str:
        """Getter for Player Marker"""
        return self._marker

    @property
    def name(self) -> str:
        """Getter for Player Name"""
        return self._name

    def __str__(self):
        """String Representation of the Player"""
        return "Player name: {} marker: {}".format(self.name, self.marker)
