# Item 7: Prefer enumerate Over range

airfoils = ["NACA0012", "NACA2412", "NACA4412"]

print("Using range:")
for i in range(len(airfoils)):
    print(i + 1, airfoils[i])

print("Using enumerate:")
for i, name in enumerate(airfoils, start=1):
    print(i, name)
