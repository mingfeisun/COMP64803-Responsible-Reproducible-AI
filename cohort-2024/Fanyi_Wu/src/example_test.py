import time
from main_solver import solve_sudoku

# grid of 9x9 but with all zeros (empty grid)
grid = [[0, 0, 0, 0, 0, 7, 0, 0, 0],
 [0, 0, 0, 0, 0, 9, 5, 0, 4],
 [0, 0, 0, 0, 5, 0, 1, 6, 9],
 [0, 8, 0, 0, 0, 0, 3, 0, 5],
 [0, 7, 5, 0, 0, 0, 2, 9, 0],
 [4, 0, 6, 0, 0, 0, 0, 8, 0],
 [7, 6, 2, 0, 8, 0, 0, 0, 0],
 [1, 0, 3, 9, 0, 0, 0, 0, 0],
 [0, 0, 0, 6, 0, 0, 0, 0, 0]]

start_time = time.time()
solved = solve_sudoku(grid)
end_time = time.time()
total_time = end_time - start_time
if solved:
    print("Puzzle solved!")
    for row in grid:
        print(row)
    print("Total time for backtracking algorithm: {:.6f} seconds".format(total_time))
else:
    print("Puzzle could not be solved.")
