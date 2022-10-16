import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the cycle collides
    with the energy, or the cycle collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._who_lost = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_energy_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_energy_collision(self, cast):
        """Updates the score nd moves the energy if the cycle collides with the energy.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        scores = cast.get_actors("scores")
        energy = cast.get_first_actor("energys")
        cycles = cast.get_actors("cycles")
        head1 = cycles[0].get_head()
        head2 = cycles[1].get_head()

        if head1.get_position().equals(energy.get_position()):
            points = energy.get_points()
            cycles[0].grow_trail(points)
            scores[0].add_points(points)
            energy.reset()

        if head2.get_position().equals(energy.get_position()):
            points = energy.get_points()
            cycles[1].grow_trail(points)
            scores[1].add_points(points)
            energy.reset()
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the cycle collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycles = cast.get_actors("cycles")
        head1 = cycles[0].get_head()
        head2 = cycles[1].get_head()
        segments = cycles[0].get_segments()[1:]+cycles[1].get_segments()[1:]
        
        for segment in segments:
            if head1.get_position().equals(segment.get_position()) or head1.get_position() == head2.get_position():
                self._is_game_over = True
                self._who_lost = 0
            
            if head2.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._who_lost = 1
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the cycle and energy white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycles = cast.get_actors("cycles")
            segments = cycles[self._who_lost].get_segments()
            energy = cast.get_first_actor("energys")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over! Player "+str(self._who_lost+1)+" lost")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments:
                segment.set_color(constants.WHITE)
            energy.set_color(constants.WHITE)