import random
import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Energy(Actor):
    """
    A tasty item that cycles like to eat.
    
    The responsibility of energy is to select a random position and points that it's worth.

    Attributes:
        _points (int): The number of points the energy is worth.
    """
    def __init__(self):
        "Constructs a new energy."
        super().__init__()
        self._points = 0
        self.set_text("@")
        self.set_color(constants.RED)
        self.reset()
        
    def reset(self):
        """Selects a random position and points that the energy is worth."""
        self._points = random.randint(1, 8)
        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(1, constants.ROWS - 1)
        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)
        self.set_position(position)
        
    def get_points(self):
        """Gets the points the energy is worth.
        
        Returns:
            points (int): The points the energy is worth.
        """
        return self._points