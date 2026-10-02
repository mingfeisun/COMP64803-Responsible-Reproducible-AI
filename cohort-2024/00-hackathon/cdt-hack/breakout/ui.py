# https://www.geeksforgeeks.org/create-breakout-game-using-python/
import time
import random
from turtle import Turtle

FONT = ("Courier", 52, "normal")
FONT2 = ("Courier", 32, "normal")
ALIGNMENT = "center"
COLOR_LIST = [
    "light blue", "royal blue", "light steel blue", "steel blue",
    "light cyan", "light sky blue", "violet", "salmon", "tomato",
    "sandy brown", "purple", "deep pink", "medium sea green", "khaki"
]


class UI(Turtle):
    """Handles the user interface elements such as game title, pause status, and game over message."""

    def __init__(self) -> None:
        """
        Initializes the UI by setting its appearance and displaying the game title.
        """
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color(random.choice(COLOR_LIST))
        self.header()

    def header(self) -> None:
        """
        Displays the game title at a fixed position.
        """
        self.clear()
        self.goto(x=0, y=-150)
        self.write("Breakout", align=ALIGNMENT, font=FONT)
        self.goto(x=0, y=-180)

    def change_color(self) -> None:
        """
        Changes the color of the UI text and re-displays the game title.
        """
        self.clear()
        self.color(random.choice(COLOR_LIST))
        self.header()

    def paused_status(self) -> None:
        """
        Displays a temporary pause effect by changing color and delaying execution.
        """
        self.clear()
        self.change_color()
        time.sleep(0.5)

    def game_over(self, win: bool) -> None:
        """
        Displays the game over message.

        Args:
            win (bool): If True, displays a winning message. Otherwise, displays a game-over message.
        """
        self.clear()
        message = "You Cleared the Game" if win else "Game is Over"
        self.write(message, align=ALIGNMENT, font=FONT)
