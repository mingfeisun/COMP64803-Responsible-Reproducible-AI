# Item 20: Prefer Raising Exceptions to Returning None

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print("Returning None")

x, y = 1, 0
result = divide(x, y)

if result is None:
    print("Invalid inputs")
else:
    print("Result:", result)