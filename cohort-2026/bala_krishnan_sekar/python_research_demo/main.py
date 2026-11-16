import numpy as np

# 1. Meaningful variable names
research_data = [10, 20, 30, 40, 50]

# 2. Reusable function
def calculate_average(data):
    if not data:
        raise ValueError("Dataset cannot be empty")
    return np.mean(data)

# 3. List comprehension
high_values = [value for value in research_data if value >= 30]

# 4. Error handling
try:
    average = calculate_average(research_data)

    print("Research Data:", research_data)
    print("Average:", average)
    print("High Values:", high_values)

except ValueError as error:
    print("Error:", error)