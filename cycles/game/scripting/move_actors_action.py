from game.scripting.action import Action


class MoveActorsAction(Action):
    """
    An update action that moves the actors.
    
    The responsibility of MoveActorsAction is to tell all of the actors to move

    Attributes:
        
    """
    def execute(self, cast, script):
        """
        Overrides the execute function of Action and instead moves all the actors
        """
        actors = cast.get_actors("cycles")

        for currentActor in actors:
            currentActor.move_next()