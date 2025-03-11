# https://www.geeksforgeeks.org/create-breakout-game-using-python/
import turtle as tr
from breakout.paddle import Paddle
from breakout.ball import Ball
from breakout.scoreboard import Scoreboard
from breakout.ui import UI
from breakout.bricks import Bricks
import time
import re

import cv2
import mediapipe as mp

screen = tr.Screen()
screen.setup(width=1200, height=600)
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)

ui = UI()
ui.header()

score = Scoreboard(lives=5)
paddle = Paddle()
bricks = Bricks()

ball = Ball()

game_paused = False
playing_game = True

screen.listen()

def pause_game():
    """
    Toggles the pause game state.
    """
    global game_paused
    if game_paused:
        game_paused = False
    else:
        game_paused = True


def check_collision_with_walls():
    """
    Checks if the ball has touched the edge of the game.
    """

    global ball, score, playing_game, ui

    # detect collision with left and right walls:
    if ball.xcor() < -580 or ball.xcor() > 570:
        ball.bounce(x_bounce=True, y_bounce=False)
        return

    # detect collision with upper wall
    if ball.ycor() > 270:
        ball.bounce(x_bounce=False, y_bounce=True)
        return

    # detect collision with bottom wall
    # In this case, user failed to hit the ball 
    # thus he loses. The game resets.
    if ball.ycor() < -280:
        ball.reset()
        score.decrease_lives()
        if score.lives == 0:
            score.reset()
            playing_game = False
            ui.game_over(win=False)
            return
        ui.change_color()
        return


def check_collision_with_paddle():
    """
    Check if the ball has touched the paddle.
    """

    global ball, paddle
    # record x-axis coordinates of ball and paddle
    paddle_x = paddle.xcor()
    ball_x = ball.xcor()

    # check if ball's distance(from its middle) 
    # from paddle(from its middle) is less than
    # width of paddle and ball is below a certain 
    #coordinate to detect their collision
    if ball.distance(paddle) < 110 and -260 <= ball.ycor() <= -240:
        ball.sety(-240)  # Push the ball above the paddle to avoid re-collision

        # If Paddle is on Right of Screen
        if paddle_x > 0:
            if ball_x > paddle_x:
                # If ball hits paddles left side it
                # should go back to left
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return

        # If Paddle is left of Screen
        elif paddle_x < 0:
            if ball_x < paddle_x:
                # If ball hits paddles left side it 
                # should go back to left
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return

        # Else Paddle is in the Middle horizontally
        else:
            if ball_x > paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            elif ball_x < paddle_x:
                ball.bounce(x_bounce=True, y_bounce=True)
                return
            else:
                ball.bounce(x_bounce=False, y_bounce=True)
                return


def check_collision_with_bricks():
    """
    Check if the ball has touched the bricks.
    """
    global ball, score, bricks

    for brick in bricks.bricks:
        if ball.distance(brick) < 40:
            score.increase_score()
            brick.quantity -= 1
            if brick.quantity == 0:
                brick.clear()
                brick.goto(3000, 3000)
                bricks.bricks.remove(brick)

            # detect collision from left
            if ball.xcor() < brick.left_wall:
                ball.bounce(x_bounce=True, y_bounce=False)

            # detect collision from right
            elif ball.xcor() > brick.right_wall:
                ball.bounce(x_bounce=True, y_bounce=False)

            # detect collision from bottom
            elif ball.ycor() < brick.bottom_wall:
                ball.bounce(x_bounce=False, y_bounce=True)

            # detect collision from top
            elif ball.ycor() > brick.upper_wall:
                ball.bounce(x_bounce=False, y_bounce=True)

def get_head_x(mp_detection: mp.solutions.face_detection, cap: cv2.VideoCapture, mp_drawing: mp.solutions.drawing_utils, x:float) -> float:
    """
    Gets the x position of the head from the camera input.

    Args:
        mp_detection (mp.solutions.face_detection): The tool to detect head.
        cap (cv2.VideoCapture): The camera input.
        mp_drawing (mp.solutions.drawing_utils): The tool to draw the head overlay.
        x (float): Last x position detected of the head.

    Returns:
        float: The new x position of the head.
    """
    
    with mp_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        success, image = cap.read()
        image.flags.writeable = False
        image.setflags(write=True)
        results = face_detection.process(image)
        if results.detections:
            detection = results.detections[0]
            # TODO: MAKE PROPER X NOT STRING REGEX
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(detection.location_data.relative_keypoints[0]))
            x, y = map(float, numbers)
            mp_drawing.draw_detection(image, detection)
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
    return x

def get_hand_x(mp_detection: mp.solutions.hands, cap: cv2.VideoCapture, mp_drawing: mp.solutions.drawing_utils, mp_drawing_styles: mp.solutions.drawing_styles, x:float) -> float:
    """
    Gets the x position of the hand from the camera input.

    Args:
        mp_detection (mp.solutions.hands): The tool to detect hands.
        cap (cv2.VideoCapture): The camera input.
        mp_drawing (mp.solutions.drawing_utils): The tool to draw the hands overlay.
        mp_drawing_styles (mp.solutions.drawing_styles): The style of hand overlay to be drawn.
        x (float): Last x position detected of the hand.

    Returns:
        float: The new x position of the hand.
    """
    with mp_detection.Hands(max_num_hands=1, min_detection_confidence=0.5) as hand_detection:
        success, image = cap.read()
        image.flags.writeable = False
        image.setflags(write=True)
        results = hand_detection.process(image)
        if results.multi_hand_landmarks:
            for detection in results.multi_hand_landmarks:
                # TODO: MAKE PROPER X NOT STRING REGEX
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(detection.landmark[0]))
                x, y, z, _ = map(float, numbers)
                mp_drawing.draw_landmarks(
                    image,
                    detection,
                    mp_detection.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
    return x

def play_main_game(controller:str = "head"):
    """
    Launch the breakout game.

    Args:
        controller (str, optional): Set to use head or hand for the controller. Defaults to "head".
    """

    if controller == "head":
        mp_detection = mp.solutions.face_detection
    else:
        mp_detection = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    x = None

    cap = cv2.VideoCapture(0)
    while playing_game:

        if not game_paused:
            if controller == "head":
                x = get_head_x(mp_detection, cap, mp_drawing, x)
            else:
                x = get_hand_x(mp_detection, cap, mp_drawing, mp_drawing_styles, x)
            # UPDATE SCREEN WITH ALL THE MOTION THAT HAS HAPPENED
            screen.update()
            time.sleep(0.01)
            ball.move()

            # DETECTING COLLISION WITH WALLS
            check_collision_with_walls()

            # DETECTING COLLISION WITH THE PADDLE
            check_collision_with_paddle()

            # DETECTING COLLISION WITH A BRICK
            check_collision_with_bricks()

            if x:
                if x > 0.55:
                    paddle.move_left()
                elif x < 0.45:
                    paddle.move_right()
            
            # DETECTING USER'S VICTORY
            if len(bricks.bricks) == 0:
                ui.game_over(win=True)
                break

        else:
            ui.paused_status()

    cap.release()
    tr.mainloop()

if __name__ == "__main__":
    play_main_game("head")