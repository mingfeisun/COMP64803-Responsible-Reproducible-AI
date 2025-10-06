"""!@file check_input.py
@brief Module containing a function for validating Sudoku grids.

@details This module contains functions for validating the structure and correctness of Sudoku grids.
It includes a function that checks whether a given grid is a valid 9x9 Sudoku grid, ensuring that each cell contains an integer between 0 and 9 and that there are no duplicates in rows, columns, or 3x3 subgrids, except for the number 0.

@author Created by F. Wu on 30/11/2023
"""

def validate_grid(grid):
    """
    @brief Validate a Sudoku grid (the form is valid and solvable).

    @details This function checks if the provided grid is a valid 9x9 Sudoku grid. It ensures that:
    - The grid is a list of 9 rows, where each row is a list of 9 numbers.
    - Each cell in the grid contains an integer value between 0 and 9 (inclusive).
    - There are no duplicate numbers in any row, column, or 3x3 subgrid, excluding the number 0.
    If any of these conditions are not met, a ValueError is raised with an appropriate message.

    @param grid A 9x9 grid represented as a list of rows, where each row is a list of integers from 0 to 9.

    @raisewarning ValueError If the grid is not a list of 9 rows, if any row is not a list of 9 integers,
            if any cell contains a value not in the range 0-9, or if duplicates are found in a row,
            column, or 3x3 subgrid (excluding zeros).
    """
    if not isinstance(grid, list) or len(grid) != 9:
        raise ValueError("validate_grid: Grid must be a list of 9 rows.")

    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            raise ValueError("validate_grid: Each row in the grid must be a list of 9 numbers.")

        for cell in row:
            if not isinstance(cell, int):
                raise ValueError("validate_grid: Grid must only contain integers.")
            if cell < 0 or cell > 9:
                raise ValueError("validate_grid: Grid numbers must be between 0 and 9, inclusive.")

    # checking for duplicates in rows, columns, and subgrids
    for i in range(9):
        row = set()
        col = set()
        subgrid = set()
        for j in range(9):
            if grid[i][j] in row and grid[i][j] != 0:
                raise ValueError(f"validate_grid: Duplicate number {grid[i][j]} found in row {i}.")
            row.add(grid[i][j])

            if grid[j][i] in col and grid[j][i] != 0:
                raise ValueError(f"validate_grid: Duplicate number {grid[j][i]} found in column {i}.")
            col.add(grid[j][i])

            row_index = 3 * (i // 3)
            col_index = 3 * (i % 3)
            if grid[row_index + j // 3][col_index + j % 3] in subgrid and grid[row_index + j // 3][col_index + j % 3] != 0:
                raise ValueError(f"validate_grid: Duplicate number {grid[row_index + j // 3][col_index + j % 3]} found in the 3x3 subgrid starting at ({row_index}, {col_index}).")
            subgrid.add(grid[row_index + j // 3][col_index + j % 3])
