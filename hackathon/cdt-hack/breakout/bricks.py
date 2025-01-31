# https://www.geeksforgeeks.org/create-breakout-game-using-python/
from turtle import Turtle
import random
from typing import List

COLOR_LIST = [
    'light blue', 'royal blue', 'light steel blue', 'steel blue',
    'light cyan', 'light sky blue', 'violet', 'salmon', 'tomato',
    'sandy brown', 'purple', 'deep pink', 'medium sea green', 'khaki'
]

weights = [
    1, 2, 1, 1, 3, 2, 1, 4, 1, 3,
    1, 1, 1, 4, 1, 3, 2, 2, 1, 2,
    1, 2, 1, 2, 1
]


class Brick(Turtle):
    """Represents a single brick in the Breakout game."""

    def __init__(self, x_cor: int, y_cor: int) -> None:
        """
        Initializes a Brick object at a specified position.

        Args:
            x_cor (int): The x-coordinate of the brick.
            y_cor (int): The y-coordinate of the brick.
        """
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(stretch_wid=1.5, stretch_len=3)
        self.color(random.choice(COLOR_LIST))
        self.goto(x=x_cor, y=y_cor)

        self.quantity: int = random.choice(weights)

        self.left_wall: int = self.xcor() - 30
        self.right_wall: int = self.xcor() + 30
        self.upper_wall: int = self.ycor() + 15
        self.bottom_wall: int = self.ycor() - 15


class Bricks:
    """Handles the creation and storage of multiple bricks in the Breakout game."""

    def __init__(self) -> None:
        """
        Initializes the Bricks manager and creates all brick lanes.
        """
        self.y_start: int = 0
        self.y_end: int = 240
        self.bricks: List[Brick] = []
        self.create_all_lanes()

    def create_lane(self, y_cor: int) -> None:
        """
        Creates a single horizontal lane of bricks at a given y-coordinate.

        Args:
            y_cor (int): The y-coordinate for the brick lane.
        """
        for i in range(-570, 570, 63):
            brick = Brick(i, y_cor)
            self.bricks.append(brick)

    def create_all_lanes(self) -> None:
        """
        Creates all lanes of bricks within the predefined y-range.
        """
        for i in range(self.y_start, self.y_end, 32):
            self.create_lane(i)
