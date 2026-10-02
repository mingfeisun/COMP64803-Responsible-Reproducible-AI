# Breakout Game with Head/Hand Tracking Controls

This is a Python implementation of the classic **Breakout** game with **MediaPipe-based head and hand tracking** for paddle control.

## Features

- Classic **Breakout** mechanics with bricks, paddle, and ball
- **Head or Hand Tracking** using **MediaPipe**
- **Collision detection** with walls, paddle, and bricks
- **Dynamic UI effects** such as color changes and game-over messages
- **Scoring system** with high score tracking

## Requirements

Make sure you have **Python 3.8+** installed and install the required dependencies:

```sh
pip install opencv-python mediapipe sphinx sphinx_rtd_theme
```

## How to Play

1. Run the game using:

   ```sh
   python -m breakout.main
   ```

2. **Choose a controller**:
   - Set `controller = "head"` to use **head movement** for paddle control.
   - Set `controller = "hand"` to use **hand movement** instead.

3. **Game Controls**:
   - Move your **head or hand** left/right to control the paddle.
   - Press **any key** to pause/unpause the game.

## File Structure

```
breakout/
├── ball.py          # Ball mechanics
├── bricks.py        # Brick setup and collision handling
├── paddle.py        # Paddle movement logic
├── scoreboard.py    # Score tracking and lives system
├── ui.py            # UI elements (title, game-over messages, colors)
└── main.py          # Main game loop and MediaPipe integration
```

## Implementation Details

- Uses **Turtle graphics** for rendering.
- **MediaPipe** is used to detect the user's **head or hand position** via webcam.
- The paddle moves based on the **normalized x-coordinate** from MediaPipe detections.
- The ball follows **simple physics rules** and bounces off surfaces.
- The game **pauses** when a key is pressed.
- For more information check out the **docs** in docs/build/html/. To generate these docs run ```make clean``` then ```make html```

## Future Improvements

- Improve **collision detection** accuracy.
- Implement **power-ups** and additional game mechanics.

## Acknowledgments

Based on the **GeeksforGeeks Breakout tutorial**:  
[Create Breakout Game Using Python](https://www.geeksforgeeks.org/create-breakout-game-using-python/)

---

Enjoy the game! 🎮🚀
``` 