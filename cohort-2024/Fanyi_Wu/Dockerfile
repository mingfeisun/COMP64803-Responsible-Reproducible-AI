# Use the base image with Miniconda
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /usr/SudokuSolver

# Copy the current directory contents into the container
COPY . .

# Update the environment using the environment.yml file
RUN conda env update -n sudoku-solver-env -f environment.yml

# Make RUN commands use the base environment
SHELL ["conda", "run", "-n", "sudoku-solver-env", "/bin/bash", "-c"]

# The code to run when container is started
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "sudoku-solver-env", "python", "src/solve_sudoku.py", "tests/input.txt"]
