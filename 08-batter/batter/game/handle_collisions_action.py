""" HandleCollisionsAction module
Contains HandleCollisionsAction class and associated utilities. Used in
controlling the gameplay and managing collisions in-game.
"""
import random
from game import constants
from game.action import Action
from game.point import Point
from game.score import Score

class HandleCollisionsAction(Action):
    """A code template for handling collisions. The responsibility of this class of objects is to update the game state when actors collide.
    
    Stereotype:
        Controller
    """
    def __init__(self):
        """The class constructor."""
        super().__init__()
        self._points = 0
        self.keep_playing = True
        self.gameWon = False

    def execute(self, cast):
        """Executes the action using the given actors.

        Args:
            cast (dict): The game actors {key: tag, value: list}.
            self.keep_playing (bool) determines whether or not to keep playing
        """
        #set values
        ball = cast["ball"][0] # ball 
        paddle = cast["paddle"][0] # paddle
        bricks = cast["brick"] # brick
        self.bricks = bricks
        score = cast["score"][0] #score

        #start brick check loop
        iterator = 0
        self.checkWin()
        for brick in bricks:
            if ball.get_position().equals(brick.get_position()):
                newDirection = ball.get_velocity().reverse_y()
                newDirection = newDirection.collision_randomizer() #randomizes the x value that comes from a y flip.
                ball.set_velocity(newDirection)
                del bricks[iterator] #need to actually delete the brick object, or it'll bounce always        
                score.add_points(1)
            iterator += 1           

        # wall and ceiling/floor check
        edgeCheck = ball.get_position().get_x()
        ceilingCheck = ball.get_position().get_y()

        if edgeCheck == constants.MAX_X - 1 or edgeCheck == 1:
            newDirection = ball.get_velocity().reverse_x()
            ball.set_velocity(newDirection)

        if ceilingCheck == 1:
            newDirection = ball.get_velocity().reverse_y()
            newDirection = newDirection.collision_randomizer()
            ball.set_velocity(newDirection)

        if ceilingCheck == constants.MAX_Y - 1:
            self.keep_playing = False

        #paddle check
        for i in range(11): #Handles collision with Paddle

            checkPosition = paddle.get_position()
            newPositionToCheck = checkPosition.lengthen_detect(i)

            if ball.get_position().equals(newPositionToCheck):
                # invert the velocity
                newDirection = ball.get_velocity().reverse_y()
                newDirection = newDirection.collision_randomizer()
                ball.set_velocity(newDirection)


    def checkGameOver(self):
        """Gets the self.keep_playing variable to run check.

        Returns:
            Boolean: Whether the game has ended.
        """
        return self.keep_playing

    def checkWin(self):
        """Checks the state of the brick in bricks.

        Args:
            self.keep_playing (Bool)
            self.gameWon (Bool)
        """
        if (len(self.bricks) == 0):
            self.keep_playing = False
            self.gameWon = True

    def getWinCondition(self):
        """Gets the self.gameWon variable based on checkWin().

        Returns:
            Boolean: If the game is won.
        """
        return self.gameWon