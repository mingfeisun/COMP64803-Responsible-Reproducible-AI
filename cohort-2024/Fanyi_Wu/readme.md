# Sudoku Solver Project

## Description & Motivation
The Sudoku Solver is an efficient tool designed to automatically solve Sudoku puzzles in a single command.
The project is motivated by the challenge of implementing a complex algorithm in a user-friendly application. The development of the Sudoku solver followed a rigorous software development strategy. Morover, caching optimisation was implemented to improve the efficiency of the backtracking algorithm used by the Sudoku solver. For comparison, constrain propagation algrithm was developed and stored in **Constraint_Propagation** branch.


## Contents
- [Installation](#installation)
- [Usage](#Usage)
- [Features](#features)
- [Frameworks](#frameworks)
- [Credits](#credits)
- [Generation Tools](#generation-tools)
- [ChatGPT and Copiot](#generation-tools)

## Installation
The project is uploaded in gitLab. To install the application, clone the repository:
```bash
git clone https://github.com/Fanyi-Kaitlyn-Wu/Good_Practice.git
```
Navigate to the project directory and install the dependencies.

### Dependencies
This project is written in Python (The project was developed using python=3.9.18). To run the project,
**Python 3** or later need to be installed.
Necessary packages used in the project are listes in environment.yml. They are:

- [numpy](https://numpy.org/) - A fundamental package for scientific computing in Python.

for unit tests:

- [pytest](https://docs.pytest.org/en/stable/) - A framework for writing small tests for Python code.


for evaluating solver performances:

- [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile) - A profiler for Python programs to analyze performance.
- [memory_profiler](https://pypi.org/project/memory-profiler/) - A module for monitoring memory usage of a Python program.

The time profile and memory profile of the Sudoku solver were save in `Profiles` folder.

for generating offline documentation:

- [doxygen](http://www.doxygen.nl/) - A tool for generating documentation from annotated code.

You can check that things are working by running tests/ (also ran by .pre-commit-config.yaml for continuous integration):

```bash
$ pytest tests/
```

## Usage
To solve a Sudoku puzzle, run the 'solve_sudoku.py' file in a single command line with the path to the puzzle file as an argument:
```bash
$ python src/solve_sudoku.py input.txt
```
The input.txt file should only include one Sudoku puzzle and in the format below:
```bash
$ cat input.txt
000|007|000
000|009|504
000|050|169
---+---+---
080|000|305
075|000|290
406|000|080
---+---+---
762|080|000
103|900|000
000|600|000
```

Make sure you are in the project directory when running the command. The solver `solve_sudoku.py` is inside the `src` folder, and the `input.txt` file should in the project directory. The solved puzzle will be saved to `output.txt` in the project directory.

The output terminal will display the solved puzzle and the time taken for the solving process:
```
solve_sudoku: Puzzle solved!
Validation time: 0.000095 seconds
Find empty time: 0.008957 seconds
Total time for backtracking algorithm: 0.046386 seconds
594|167|832
618|239|574
237|458|169
---+---+---
981|726|345
375|841|296
426|395|781
---+---+---
762|584|913
143|972|658
859|613|427
```
If an invalid or unsolvable puzzle is give to the solver, corresponding and informative error messages will be displayed.

- For invalid input grid:
```
validate_grid: Grid must be a list of 9 rows.
Puzzle could not be solved.
```

- For unsolvable puzzle:
```
validate_grid: Duplicate number 8 found in the 3x3 subgrid starting at (3, 6).
Puzzle could not be solved.
```

## Features
- **Puzzle Solving**: Solves standard 9x9 Sudoku puzzles.
- **File I/O**: Reads puzzles from and writes solutions to text files. Both of the .txt files are in the project directory and have the same format of Sudoku grid.
- **Efficiency Evaluation**: Measures and displays the time taken for key steps (validating the grid, finding empty cells and the main solver) in the solving process.
- **CLI Interface**: Offers a simple command-line interface for ease of use.

## Frameworks
- **Language**: Python 3.9.18
- **Testing**: PyTest for unit tests (in `tests` folder: `test_check_input.py`, `test_find_empty.py`, `test_is_valid.py`)
```bash
$ pytest tests/
```
- **CI**: GitHub Actions for continuous integration and automated pytest (unit test) before each commit. The `pre-commit-config.yaml` file was employed to automate checks before committing changes.
- **Containerisation**: Docker was used for reproducing the project. Key configurations include continuumio/miniconda3 as the base image for a Miniconda-based Python environment. It sets /usr/SudokuSolver as the working directory, and copies all project files into the container. The environment is set up by executing conda env update using the `environment.yml` file, and the Docker shell is configured to use the sudoku-solver-env. It is runnable by using the single command:
```bash
docker run sudoku-solver
```

## Credits
Author: Fanyi Wu

## Generation Tools
- [VSCode](https://code.visualstudio.com/) - Python IDE for development.
- [Git](https://git-scm.com/) - Version control system for managing code versions and collaboration.
- [Docker](https://www.docker.com/) - Containerization platform for ensuring consistent environments.
- [Doxygen](https://www.doxygen.nl/index.html) - Documentation generator tool used for writing software documentation from annotated source code.
- [Copilot](https://github.com/features/copilot) - Autofill codes and debug for the scripts.


## ChatGPT (https://www.chat.openai.com/)
AI generation tool used to help with developing and embellishing the project.

**Prototyping**

prompt:
- What are the logics of backtracking and constraint propagation algorithms when solving a Sudoku?

The results are used to help draft the prototype. Using the logic, the structure of the main solver and the corresponding fundamental modules in src folder (`check_input`, `find_empty`, `is_valid`) were developed.

**Developing**

prompt:
- For `check_input.py`, try to reduce the loops used to check for the conditions.

The result was used to optimise and concise the code. Before the optimisation by ChatGPT:
```
if not isinstance(row, list):
    raise ValueError("validate_grid")

else:
    length_count = 0

    for element in row:
        length_count += 1

    if length_count != 9:
        raise ValueError("validate_grid")
```
After using ChatGPT, the above code condensed to:
```
if not isinstance(row, list) or len(row) != 9:
    raise ValueError("validate_grid")
```

- For `find_empty.py`, how to optimise the searching algorithm using cache optimisation?

The result provided an insight of maintaining a cache of empty cells. This cache is updated whenever a cell in the Sudoku grid is modified. The key idea is to avoid scanning the entire grid every time we need to find an empty cell. This was used to optimise the code in `find_empty.py`.

- Debug the code.

The result was used to debug the code and make the code more robust.

**Formatting**
- For the docstrings, revise for grammar mistakes and make sure they are compatible with Doxygen. Do not change the logic and wording.

The result was used to clarify and beautify the docstrings.

- Give me a general outlines for things to mention in the README file.

The result was used to structure the README.md file for the project.
