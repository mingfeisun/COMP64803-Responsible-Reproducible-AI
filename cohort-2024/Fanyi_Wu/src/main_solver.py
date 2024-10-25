"""!@file main_solver.py
 @brief Module for solving Sudoku puzzles (in the form of 2D list).

 @details This module imports necessary functions and classes for solving Sudoku puzzles.
 It includes a primary function `solve_sudoku` which attempts to solve the puzzle using a backtracking algorithm.
 Then it utilizes `validate_grid` for initial grid validation, `SudokuSolverWithCache` for managing the puzzle state,
 and `is_valid` for checking the validity of each move.

 The module is designed to measure the time taken for validation
 and finding empty cells, providing insights into the performance of the solving process.
 Optional profiling lines are commented out for further performance analysis.

 @author Created by F. Wu on 30/11/2023
"""

import time
from check_input import validate_grid
from find_empty import SudokuSolverWithCache
from is_valid import is_valid
# from memory_profiler import profile
# import cProfile

# @profile(precision=4)
def solve_sudoku(grid, validation_times=[], find_empty_times=[]):
    """
    @brief Solve a Sudoku puzzle using a backtracking algorithm.

    @details This function attempts to solve a Sudoku puzzle. It first validates the input grid,
    then proceeds to solve the puzzle using a backtracking algorithm implemented in the `SudokuSolverWithCache` class.
    The function measures the time taken for grid validation and finding empty cells, which are appended to respective lists.
    The function prints messages regarding the puzzle's completeness and solvability.

    @param grid A 2D list representing the initial Sudoku grid.
    @param validation_times A list to store the time taken for grid validation at each call (default empty).
    @param find_empty_times A list to store the time taken to find empty cells at each call (default empty).

    @return A tuple containing a boolean indicating if the puzzle was solved or not, and the lists `validation_times` and `find_empty_times`.

    @exception ValueError If the input grid is not valid.

    @note The commented out lines are for optional profiling (both time profile and memory profile).


    Example Usage: The following code snippet demonstrates how to use solve_sudoku function.
    ```
    initial_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    solved, validation_times, find_empty_times = solve_sudoku(initial_grid)
    print("Sudoku Solved:", solved)
    ```
    """

    try:
        start_time = time.time()
        validate_grid(grid)
        validation_times.append(time.time() - start_time)
    except ValueError as e:
        print(e)
        return False, validation_times, find_empty_times

    solver = SudokuSolverWithCache(grid)

    start_time = time.time()
    find = solver.find_empty()
    find_empty_times.append(time.time() - start_time)
    if not find:
        print("solve_sudoku: No empty cells found. The grid might already be complete.")
        return True, validation_times, find_empty_times

    def backtrack():
        start_time = time.time()
        find = solver.find_empty()  # Use the cached method to find an empty cell
        find_empty_times.append(time.time() - start_time)

        if not find:
            return True  # Puzzle solved

        row, col = find
        for num in range(1, 10):
            if is_valid(grid, row, col, num):
                solver.update_cell(row, col, num)  # Update the cell in the solver's grid

                if backtrack():
                    return True  # Puzzle solved

                solver.update_cell(row, col, 0)  # Backtrack in the solver's grid

        return False  # Puzzle not solved

    # Start solving the puzzle
    if backtrack():
        print("solve_sudoku: Puzzle solved!")
    else:
        print("solve_sudoku: Puzzle could not be solved.")

    return True, validation_times, find_empty_times

# from grid_file import read_grid_file

# # Read the soduku grid from a file
# file_path = '/Users/kaitlyn/DIS/Research_Computing/fw385/tests/input.txt'
# grid = read_grid_file(file_path)
# if __name__ == '__main__':
#     solve_sudoku(grid)

# # cProfile.run('solve_sudoku(grid)')
