import sys
import os
import time

# Add the 'src' directory to the sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from main_solver import solve_sudoku

grid = [
    [5, 1, 6, 8, 0, 9, 0, 3, 2],
    [3, 2, 0, 6, 7, 1, 8, 9, 0],
    [8, 0, 9, 2, 0, 4, 5, 6, 1], # Duplicate number 5 found in the 3x3 subgrid starting at (0, 0)

    [1, 5, 3, 4, 6, 7, 0, 8, 9],
    [6, 0, 2, 0, 9, 5, 3, 0, 8],
    [9, 8, 7, 3, 2, 0, 6, 4, 5],

    [7, 6, 1, 5, 8, 3, 9, 2, 4],
    [2, 0, 4, 9, 1, 6, 0, 5, 7],  # Notice the duplicate '1' in this row
    [4, 9, 8, 7, 0, 2, 1, 1, 6]   # Notice the duplicate '1' in this row as well
]

start_time = time.time()
solved, validation_times, find_empty_times = solve_sudoku(grid)
end_time = time.time()
total_time = end_time - start_time
if solved:
    print("Puzzle solved!")
    for row in grid:
        print(row)
    print("Validation time: {:.6f} seconds".format(sum(validation_times)))
    print("Find empty time: {:.6f} seconds".format(sum(find_empty_times)))
    print("Total time for backtracking algorithm: {:.6f} seconds".format(total_time))
else:
    print("Puzzle could not be solved.")
