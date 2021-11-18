""" Director module
Contains Director class and associated utilities. Used in
controlling the gameplay and managing in-game events.
"""
from time import sleep
from game import constants, handle_collisions_action
from game.actor import Actor
from game.point import Point

class Director:
    """A code template for a person who directs the game. The responsibility of 
    this class of objects is to control the sequence of play.
    
    Stereotype:
        Controller

    Attributes:
        _cast (dictionary): The game actors {key: name, value: object}
        _script (dictionary): The game actions {key: tag, value: object}
    """

    def __init__(self, cast, script):
        """The class constructor.
        
        Args:
            cast (dict): The game actors {key: tag, value: list}.
            script (dict): The game actions {key: tag, value: list}.
        """
        self._cast = cast
        self._script = script
        self.keep_playing = True
        self.gameWon = False
        self.endingText = ""
        
    def start_game(self):
        """Starts the game loop to control the sequence of play."""
        while self.keep_playing == True:
            self._cue_action("input")
            self._cue_action("update")
            self._cue_action("output")
            self.keep_playing = self._script["update"][1].checkGameOver()
            sleep(constants.FRAME_LENGTH)

        self.gameWon = self._script["update"][1].getWinCondition() #Checks if all bricks are destroyed

        if self.gameWon == True:
            self.endingText = "You won!" #If all bricks gone, game is won.
        else:
            self.endingText = "Game Over! Try Again" #if not, game over. 

        self._cast = {} #deletes all displayed objects

        x = int((constants.MAX_X / 2) - 5)
        y = int((constants.MAX_Y  / 2) - 1)
        position = Point(x, y)
        endingScreen = Actor() #creates new object to display - Ending Screen

        endingScreen.set_text(self.endingText)
        endingScreen.set_position(position)

        self._cast["endingScreen"] = [endingScreen]

        self._cue_action("output") #displays the text object
        sleep(10) #Delays game end so text can be read.
        #end program.

    def _cue_action(self, tag):
        """Executes the actions with the given tag.
        
        Args:
            tag (string): The given tag.
        """ 
        for action in self._script[tag]:
            action.execute(self._cast)