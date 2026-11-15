"""Run the five demos one after the other.

Run it from the project folder with  python run_all.py
"""
import pathlib
import platform
import runpy
import sys
import time

# Print the exact Python version first, so results can be compared.
print(f"Python {platform.python_version()} ({sys.implementation.name}) "
      f"on {platform.system()} {platform.machine()}")

start = time.perf_counter()
folder = pathlib.Path(__file__).parent / "snippets"
for path in sorted(folder.glob("way*.py")):
    print()
    runpy.run_path(str(path), run_name="__main__")

print(f"\nAll five demos ran in {time.perf_counter() - start:.1f} s. "
      "Times change from one machine to another.")
