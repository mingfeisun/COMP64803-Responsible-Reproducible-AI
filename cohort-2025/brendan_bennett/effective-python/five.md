Imagine you have a big file called app.py that handles:

- user data
- math utilities
- and a main program loop

This can be broken down

```
my_project/
│
├── main.py              # Entry point of the program
│
├── user/
│   ├── __init__.py      # Makes this a package
│   ├── models.py        # Defines dataclasses or classes for users
│   └── utils.py         # Helper functions for user management
│
└── math_utils/
    ├── __init__.py
    ├── operations.py    # Arithmetic functions
    └── statistics.py    # Functions for averages, variance, etc.
```

and accessed
```python
#main.py
from user.models import User
from math_utils.operations import add, multiply

def main():
    u = User(name="Alice", age=30)
    print(f"User: {u}")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"2 × 3 = {multiply(2, 3)}")

if __name__ == "__main__":
    main()
```