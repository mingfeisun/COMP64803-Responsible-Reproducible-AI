# https://www.geeksforgeeks.org/create-breakout-game-using-python/
from turtle import Turtle

try:
    score = int(open('highestScore.txt', 'r').read())
except FileNotFoundError:
    score = open('highestScore.txt', 'w').write(str(0)) or 0
except ValueError:
    score = 0

FONT = ('Arial', 18, 'normal')


class Scoreboard(Turtle):
    """Represents the scoreboard for tracking the player's score and lives."""

    def __init__(self, lives: int) -> None:
        """
        Initializes the Scoreboard with a given number of lives.

        Args:
            lives (int): The initial number of lives.
        """
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.highScore: int = score
        self.goto(x=-580, y=260)
        self.lives: int = lives
        self.score: int = 0
        self.update_score()

    def update_score(self) -> None:
        """
        Updates the displayed score, high score, and remaining lives.
        """
        self.clear()
        self.write(
            f"Score: {self.score} | Highest Score: {self.highScore} | Lives: {self.lives}",
            align='left',
            font=FONT
        )

    def increase_score(self) -> None:
        """
        Increases the player's score and updates the high score if necessary.
        """
        self.score += 1
        if self.score > self.highScore:
            self.highScore = self.score
        self.update_score()

    def decrease_lives(self) -> None:
        """
        Decreases the player's lives by one and updates the display.
        """
        self.lives -= 1
        self.update_score()

    def reset(self) -> None:
        """
        Resets the score to zero and updates the high score file.
        """
        self.clear()
        self.score = 0
        self.update_score()
        with open('highestScore.txt', 'w') as file:
            file.write(str(self.highScore))
