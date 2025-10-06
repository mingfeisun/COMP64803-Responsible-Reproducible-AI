"""!@file is_valid.py
@brief Module containing a function for validating a number placed in a cell.

@details The is_valid() function determines the validity of placing a specific number 'num' in the 'grid' at position ('row', 'col')
The function executes a series of checks to assess the validity of placing a number in a Sudoku grid to ensure it follows the Sudoku rules:
- Number must be between 1 and 9
- Number must not already exist in the given row
- Number must not already exist in the given column
- Number must not already exist in the 3x3 subgrid that includes the cell at ('row', 'col')

@author Created by F. Wu on 30/11/2023
"""

def is_valid(grid, row, col, num):
    """
    @brief Check if it's valid to place 'num' in the 'grid' at position ('row', 'col').

    @details This function checks if it's valid to place 'num' in the 'grid' at position ('row', 'col'):
    - It first determines if the cell at the specified 'row' and 'col' is empty or can accept a new value.
    - It then confirms whether the number 'num' is already present in the given 'row', followed by a check to see if 'num' exists in the specified 'col'.
    - Finally, it verifies if 'num' is already in the 3x3 subgrid that includes the cell at ('row', 'col').
    - If 'num' does not violate any of these constraints, the function returns True, signifying that it is permissible to place 'num' at the specified position.
    - If any constraint is violated, it returns False.

    @param grid (list of lists of int): The current state of the Sudoku grid.
    @param row (int): Row index where the number is to be placed.
    @param col (int): Column index where the number is to be placed.
    @param num (int): The number to place.

    @return True if placing 'num' at ('row', 'col') is valid, False otherwise.
    """
    if not (1 <= num <= 9):
        return False  # Number must be between 1 and 9

    # Check if 'num' is not in the given 'row'
    for x in range(9):
        if grid[row][x] == num:
            #raise ValueError(f"Number {num} already exists in row {row}.")
            return False

    # Check if 'num' is not in the given 'col'
    for x in range(9):
        if grid[x][col] == num:
            #raise ValueError(f"Number {num} already exists in column {col}.")
            return False

    # Calculate the start of the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)

    # Check if 'num' is not in the 3x3 subgrid
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                #raise ValueError(f"Number {num} already exists in the 3x3 subgrid starting at ({start_row}, {start_col}).")
                return False

    return True
