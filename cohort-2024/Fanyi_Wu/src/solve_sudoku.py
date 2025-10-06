"""!@file solve_sudoku.py
@brief Sudoku Solver Command Line Interface.

@details This script solves a Sudoku puzzle from an input file and saves the solution to 'output.txt'.
It uses `solve_sudoku` defined in main_solver.py module for solving, `read_grid_file` to read the puzzle, and `save_grid_file` for output.
Execution time for various stages is measured and displayed. It accepts the puzzle file path as a command-line argument.

Example Usage: $ python solve_sudoku.py [input_file_path]

@author Created by F. Wu on 30/11/2023
"""

from main_solver import solve_sudoku
from grid_file import read_grid_file
from grid_file import save_grid_file
import sys
# import cProfile
import time

# Read the input file
file_path = sys.argv[1]
grid = read_grid_file(file_path)

#cProfile.run('solve_sudoku(grid)')

start_time = time.time()
# Solve the puzzle
solved, validation_times, find_empty_times = solve_sudoku(grid)
end_time = time.time()
total_time = end_time - start_time
if solved:
    print("Validation time: {:.6f} seconds".format(sum(validation_times)))
    print("Find empty time: {:.6f} seconds".format(sum(find_empty_times)))
    print("Total time for backtracking algorithm: {:.6f} seconds".format(total_time))
else:
    print("Puzzle could not be solved.")

# Save the result to a file
save_grid_file(grid, 'output.txt')
