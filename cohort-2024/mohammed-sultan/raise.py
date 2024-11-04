from typing import Tuple, Optional

# Approach 1: Returning None (Error-prone)
def careful_divide_none(a: float, b: float) -> Optional[float]:
    """Divides a by b, returns None if division by zero occurs."""
    try:
        return a / b
    except ZeroDivisionError:
        return None

# Approach 2: Raising an Exception (Best practice)
def careful_divide_exception(a: float, b: float) -> float:
    """Divides a by b, raises ValueError if division by zero occurs."""
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Invalid inputs: division by zero")

# Testing the approaches
if __name__ == "__main__":
    x, y = 1, 0

    # Test Approach 1
    print("Approach 1: Returning None")
    result = careful_divide_none(x, y)
    if result is None:
        print("Invalid inputs (None returned)")
    else:
        print(f"Result: {result}")

    print("\nApproach 2: Raising an Exception")
    # Test Approach 2
    try:
        result = careful_divide_exception(x, y)
    except ValueError as e:
        print(e)
    else:
        print(f"Result: {result}")