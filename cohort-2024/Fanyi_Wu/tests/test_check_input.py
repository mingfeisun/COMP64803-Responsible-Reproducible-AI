import pytest
import os
import sys

# Add the 'src' directory to the sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from check_input import validate_grid
def test_valid_grid():
    # Create a valid Sudoku grid and assert that no exception is raised
    grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    validate_grid(grid)

def test_invalid_grid_size():
    grid_too_many_rows = [[0]*9]*10  # 10 rows
    grid_too_few_rows = [[0]*9]*8   # 8 rows
    grid_too_many_cols = [[0]*10]*9 # 10 columns in each row
    grid_too_few_cols = [[0]*8]*9   # 8 columns in each row

    with pytest.raises(ValueError):
        validate_grid(grid_too_many_rows)
    with pytest.raises(ValueError):
        validate_grid(grid_too_few_rows)
    with pytest.raises(ValueError):
        validate_grid(grid_too_many_cols)
    with pytest.raises(ValueError):
        validate_grid(grid_too_few_cols)

def test_invalid_data_type():
    grid_with_string = [[0]*9]*8 + [['a']*9]  # One row with strings
    grid_with_list = [[0]*9]*8 + [[[]]*9]    # One row with lists

    with pytest.raises(ValueError):
        validate_grid(grid_with_string)
    with pytest.raises(ValueError):
        validate_grid(grid_with_list)


def test_invalid_value_range():
    grid_with_invalid_number = [[0]*9]*8 + [[10]*9]  # One row with a number outside 0-9

    with pytest.raises(ValueError):
        validate_grid(grid_with_invalid_number)

def test_duplicate_values():
    grid_duplicate_row = [[0]*9]*8 + [[1]*9]  # Duplicate in the last row
    grid_duplicate_column = [[1 if i == 8 else 0 for i in range(9)] for _ in range(9)]  # Duplicate in the last column

    with pytest.raises(ValueError):
        validate_grid(grid_duplicate_row)
    with pytest.raises(ValueError):
        validate_grid(grid_duplicate_column)


def test_grid_with_zeros():
    # Create a valid grid with zeros and assert that no exception is raised
    grid = grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    validate_grid(grid)
