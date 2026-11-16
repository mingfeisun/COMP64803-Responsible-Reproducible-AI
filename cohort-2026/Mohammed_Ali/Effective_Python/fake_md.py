"""A pretend MD simulation. item52_subprocess.py runs this as a child process.

Usage: python fake_md.py <temperature> <steps> <output file>
"""
import random
import sys
import time

temperature = float(sys.argv[1])
steps = int(sys.argv[2])
output_file = sys.argv[3]

if temperature <= 0:
    print("error: temperature must be positive")
    sys.exit(1)  # a non-zero exit code means "something went wrong"

with open(output_file, "w") as f:
    for step in range(steps):
        # 10 atoms in a line, jiggling more at higher temperature
        for atom in range(10):
            x = atom + random.gauss(0, 0.1 * temperature)
            f.write(f"{step} {atom} {x:.4f}\n")
        time.sleep(0.01)  # pretend each step takes real work

print(f"finished {steps} steps at T={temperature}")
