# demo_main.py
import numpy as np

# item 5 
from demo_item5 import gaussian
print("\n=== Item 5 ===")
x = np.linspace(-10, 10, 1000)
y = gaussian(x, mu=0, sigma=1.5)
print("x values:", x)
print("Gaussian results:", np.round(y, 4))

# item 9
from demo_item9 import find_even
print("\n=== Item 9 ===")
find_even([1, 3, 5, 7])
find_even([1, 2, 3, 4])

# item 21
from demo_item21 import create_multipliers
print("\n=== Item 21 ===")
funcs = create_multipliers()
print("Multipliers applied to 2:", [f(2) for f in funcs])

# item 31
from demo_item31 import normalise
print("\n=== Item 31 ===")
data = (x for x in range(1, 4))
print("First normalisation:", normalise(data))  # [0.16666666666666666, 0.3333333333333333, 0.5]
data = (x for x in range(1, 4))
print("Second normalisation:", normalise(data))  # [0.16666666666666666, 0.3333333333333333, 0.5]

# item 88
print("\n=== Item 88 ===")
import demo_item88
