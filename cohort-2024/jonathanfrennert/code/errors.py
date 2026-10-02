def careful_divide(a, b):
    """Perform division and raise an exception for invalid inputs."""
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError('Cannot divide by zero')  # Raise exception instead of returning None

# Example usage of careful_divide
try:
    result = careful_divide(10, 0)  # This will raise an exception
except ValueError as e:
    print(f'Error: {e}')  # Handle the exception and print the error message
else:
    print(f'Result is {result}')  # This line won't execute if an exception is raised
