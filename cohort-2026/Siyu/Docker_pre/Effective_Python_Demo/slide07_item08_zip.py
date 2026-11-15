# Item 8: Use zip to process Iterators in parallel

airfoils = ["NACA0012", "NACA2412", "NACA4412"]
drags = [0.012, 0.015, 0.018]

for name, cd in zip(airfoils, drags, strict=True):
    print(name, cd)

# Different lengths cause an error with strict=True
try:
    list(zip(["A", "B"], [0.012], strict=True))
except ValueError:
    print("Lists have different lengths")
