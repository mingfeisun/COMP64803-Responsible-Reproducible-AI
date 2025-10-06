import pytest
import os
import sys

# Add the 'src' directory to the sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from find_empty import SudokuSolverWithCache

def test_initialize():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolverWithCache(grid)
    assert solver.grid == grid
    assert solver.empty_cells_cache == [(i, j) for i in range(9) for j in range(9)]

def test_find_empty_on_empty_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolverWithCache(grid)
    assert solver.find_empty() == (0, 0)

def test_find_empty_on_non_empty_grid():
    grid = [[0 if i != j else 1 for i in range(9)] for j in range(9)]
    solver = SudokuSolverWithCache(grid)
    assert solver.find_empty() == (0, 1)

def test_find_empty_none():
    grid = [[1 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolverWithCache(grid)
    assert solver.find_empty() is None

def test_update_cell_add_to_cache():
    grid = [[1 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolverWithCache(grid)
    solver.update_cell(0, 0, 0)
    assert solver.grid[0][0] == 0
    assert (0, 0) in solver.empty_cells_cache

def test_update_cell_remove_from_cache():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolverWithCache(grid)
    solver.update_cell(0, 0, 1)
    assert solver.grid[0][0] == 1
    assert (0, 0) not in solver.empty_cells_cache
