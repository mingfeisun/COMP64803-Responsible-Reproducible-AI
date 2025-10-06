# https://www.geeksforgeeks.org/create-breakout-game-using-python/
from turtle import Turtle
from breakout.ball import MOVE_DIST as BALL_MOVE_DIST

BALL_TO_PADDLE_RATIO = 3  # Ratio of ball movement to paddle movement
MOVE_DIST = BALL_MOVE_DIST * BALL_TO_PADDLE_RATIO


class Paddle(Turtle):
    """Represents the paddle in the Breakout game."""

    def __init__(self) -> None:
        """
        Initializes the Paddle object at the starting position.
        """
        super().__init__()
        self.color('steel blue')
        self.shape('square')
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=10)
        self.goto(x=0, y=-280)

    def move_left(self) -> None:
        """
        Moves the paddle left by a fixed distance.
        """
        self.backward(MOVE_DIST)

    def move_right(self) -> None:
        """
        Moves the paddle right by a fixed distance.
        """
        self.forward(MOVE_DIST)
