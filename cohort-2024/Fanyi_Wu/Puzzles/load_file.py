import sys
import os
import time

# Add the 'src' directory to the sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from main_solver import solve_sudoku
from grid_file import read_grid_file
from grid_file import save_grid_file

# Read the soduku grid from a file
file_path = '/Users/kaitlyn/DIS/Research_Computing/fw385/tests/input.txt'
grid = read_grid_file(file_path)

start_time = time.time()
solved, validation_times, find_empty_times = solve_sudoku(grid)
end_time = time.time()
total_time = end_time - start_time
if solved:
    for row in grid:
        print(row)
    print("Validation time: {:.6f} seconds".format(sum(validation_times)))
    print("Find empty time: {:.6f} seconds".format(sum(find_empty_times)))
    print("Total time for backtracking algorithm: {:.6f} seconds".format(total_time))
else:
    print("Puzzle could not be solved.")

# Save the result to a file
save_grid_file(grid, '/Users/kaitlyn/DIS/Research_Computing/fw385/tests/output.txt')
