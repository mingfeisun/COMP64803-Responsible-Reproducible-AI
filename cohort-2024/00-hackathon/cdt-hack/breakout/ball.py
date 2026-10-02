# https://www.geeksforgeeks.org/create-breakout-game-using-python/
from turtle import Turtle

MOVE_DIST: float = 5

class Ball(Turtle):
    """
    A class representing the ball in the Breakout game.
    
    Attributes:
        x_move_dist (float): Distance to move in the x-direction.
        y_move_dist (float): Distance to move in the y-direction.
    """
    
    def __init__(self) -> None:
        """Initializes the ball with default position and movement settings."""
        super().__init__()
        self.shape('circle')
        self.color('white')
        self.penup()
        self.x_move_dist: float = MOVE_DIST
        self.y_move_dist: float = MOVE_DIST
        self.reset()

    def move(self) -> None:
        """Moves the ball in the current direction."""
        new_y: float = self.ycor() + self.y_move_dist
        new_x: float = self.xcor() + self.x_move_dist
        self.goto(x=new_x, y=new_y)

    def bounce(self, x_bounce: bool, y_bounce: bool) -> None:
        """
        Reverses the direction of the ball when it collides with an obstacle.
        
        Args:
            x_bounce (bool): If True, reverses horizontal direction.
            y_bounce (bool): If True, reverses vertical direction.
        """
        if x_bounce:
            self.x_move_dist *= -1

        if y_bounce:
            self.y_move_dist *= -1

    def reset(self) -> None:
        """Resets the ball to its initial position and movement direction."""
        self.goto(x=0, y=-240)
        self.y_move_dist = MOVE_DIST
