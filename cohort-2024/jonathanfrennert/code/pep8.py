class SampleClass:
    """A sample class to demonstrate PEP 8 style guide compliance."""

    CONSTANT_VALUE = 42  # Constant should be in ALL_CAPS

    def __init__(self):
        self.__private_attribute = "I am private"  # Private attribute
        self._protected_attribute = "I am protected"  # Protected attribute
        self.public_attribute = "I am public"  # Public attribute

    def sample_method(self):
        """A sample method demonstrating PEP 8 guidelines."""
        value_a = 10
        value_b = 20
        total = (value_a + value_b + self.CONSTANT_VALUE)

        if value_a is not value_b:  # Use inline negation
            print("Values are not equal.")

        return total


def another_function():
    """Another function to show proper spacing and naming conventions."""
    result = SampleClass().sample_method()
    print(f"Total: {result}")


# Separate class and function definitions with 2 lines
# This is a new function that follows the guidelines
def yet_another_function():
    """Yet another function."""
    pass


# Main execution block
if __name__ == "__main__":
    another_function()
