import pytest
import os
import sys

# Add the 'src' directory to the sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from is_valid import is_valid

def test_is_valid_number():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    assert is_valid(grid, 0, 0, 5) == True  # Valid placement

def test_invalid_number_range():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    assert is_valid(grid, 0, 0, 10) == False  # Number out of valid range

def test_invalid_row_placement():
    grid = [[1 if i == 0 else 0 for i in range(9)] for _ in range(9)]
    assert is_valid(grid, 0, 1, 1) == False  # Invalid due to same number in row

def test_invalid_col_placement():
    grid = [[1 if j == 0 else 0 for _ in range(9)] for j in range(9)]
    assert is_valid(grid, 1, 0, 1) == False  # Invalid due to same number in column

def test_invalid_subgrid_placement():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[0][0] = 1  # Place a '1' in the top-left corner of the grid
    assert is_valid(grid, 1, 1, 1) == False  # Invalid due to same number in 3x3 subgrid

def test_valid_subgrid_placement():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[0][0] = 1  # Place a '1' in the top-left corner of the grid
    assert is_valid(grid, 1, 1, 2) == True  # Valid placement in subgrid
