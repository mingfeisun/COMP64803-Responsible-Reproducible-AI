# Item 14: Sort by Complex Criteria Using the key Parameter

runs = [
    ("NACA0012", 0.012, 40),
    ("NACA2412", 0.015, 20),
    ("NACA4412", 0.018, 15),
]

ranked = sorted(runs, key=lambda r: (r[1], r[2]))

print("Ranked designs:")
for name, cd, runtime in ranked:
    print(name, cd, runtime)

print("Lowest Cd:", ranked[0][0])
