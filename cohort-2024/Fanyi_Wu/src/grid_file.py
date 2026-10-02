"""!@file grid_file.py
@brief Module containing two functions for reading and outputting Sudoku grids.

@details This module contains two functions for reading and outputting Sudoku grids.
The read_grid_file() function reads a Sudoku grid from a text file and returns it as a list of lists of integers (2D list).
The save_grid_file() function saves a Sudoku grid to a text file, which is in the same format as the input file.

@author Created by F. Wu on 30/11/2023
"""

def read_grid_file(file_path):
    """
    @brief Read a Sudoku puzzle from input file and convert it into a 2D list.

    @details This function opens a file containing a Sudoku puzzle and parses each line into a list of integers,
    representing the Sudoku grid. This is achieved by calling parse_sudoku_line(line).

    @param file_path The path to the file containing the Sudoku puzzle.

    @return A 2D list representing the Sudoku grid, or None if there is an error in file reading
    or if the puzzle format is incorrect.

    @exception FileNotFoundError If the specified file cannot be found.
    @exception ValueError If any row in the Sudoku puzzle is not of length 9.
    @exception Exception For any other errors that occur during file reading.

    Example usage:
    To read a Sudoku grid from 'input.txt':
    ```
    grid = read_grid_file('input.txt')
    ```
    The input.txt file should only include one Sudoku puzzle and in the format below:
    ```bash
    $ cat input.txt
    000|007|000
    000|009|504
    000|050|169
    ---+---+---
    080|000|305
    075|000|290
    406|000|080
    ---+---+---
    762|080|000
    103|900|000
    000|600|000
    ```
    """
    grid = []

    def parse_sudoku_line(line):
        return [int(num) if num.isdigit() else 0 for num in line if num.isdigit()]

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Ignore lines with '---+---+---'
                if '---' not in line:
                    try:
                        # Parse the line into a list of integers
                        row = parse_sudoku_line(line)
                        if len(row) != 9:  # Each row must have exactly 9 numbers
                            raise ValueError(f"read_grid_file: Invalid row length in line: {line.strip()}")
                        grid.append(row)
                    except ValueError as ve:
                        print(ve)
                        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return grid


def save_grid_file(grid, file_path):
    """
    @brief Save a Sudoku puzzle to a file from a 2D list representation.

    @details This function writes a Sudoku grid to an output file, making the output Sudoku in the same format as the input file.
    It is achieved by calling format_sudoku_row(row)
    - converts each row into a string format with '|' separators for every three numbers.
    - After every third row (except the last one), a separator
    line '---+---+---' is added.
    - The function handles any exceptions that may occur during file writing.

    @param grid A 2D list representing the Sudoku grid.
    @param file_path The path where the Sudoku puzzle will be saved.

    @exception Exception If an error occurs while writing to the file.

    Example usage:
    To save a Sudoku grid to 'output.txt':
    ```
    save_grid_file(grid, 'output.txt')
    ```
    The output.txt file will be in the same format as the input.txt file.
    """

    def format_sudoku_row(row):
        """Convert a row of the Sudoku grid to the string format with '|' separators."""
        return '|'.join(''.join(str(num) if num != 0 else '0' for num in row[i:i+3]) for i in range(0, 9, 3))

    try:
        with open(file_path, 'w') as file:
            for i, row in enumerate(grid):
                formatted_row = format_sudoku_row(row)
                file.write(formatted_row + '\n')
                print(formatted_row)
                # Add a separator line after every third row, except the last one
                if i % 3 == 2 and i != 8:
                    file.write('---+---+---\n')
                    print('---+---+---')
    except Exception as e:
        print(f"save_grid_file: An error occurred while writing to the file: {e}")
