"""Item 30: Consider generators instead of returning lists.

Reads a big trajectory file two ways and works out the same average:
  - as a list:       load every frame into memory first
  - as a generator:  hand over one frame at a time

Run: python item30_generators.py
"""
import random
import tracemalloc

FILE = "big_trajectory.txt"
N_FRAMES = 2000
N_ATOMS = 100


def write_fake_trajectory():
    """Make a test file: one line per atom, N_ATOMS lines per frame."""
    with open(FILE, "w") as f:
        for frame in range(N_FRAMES):
            for atom in range(N_ATOMS):
                x, y, z = random.random(), random.random(), random.random()
                f.write(f"{frame} {x:.4f} {y:.4f} {z:.4f}\n")


def read_frames_as_list(path):
    """Read the WHOLE file and return a list holding every frame."""
    frames = []
    current = []
    with open(path) as f:
        for line in f:
            _, x, y, z = line.split()
            current.append((float(x), float(y), float(z)))
            if len(current) == N_ATOMS:  # frame complete
                frames.append(current)
                current = []
    return frames


def read_frames_one_at_a_time(path):
    """The same, but a generator: `yield` hands back one frame and pauses."""
    current = []
    with open(path) as f:
        for line in f:
            _, x, y, z = line.split()
            current.append((float(x), float(y), float(z)))
            if len(current) == N_ATOMS:
                yield current  # give this frame to the caller, then carry on
                current = []


def average_x(frames):
    """Works with a list OR a generator: it just loops over frames."""
    total = 0.0
    count = 0
    for frame in frames:
        for x, y, z in frame:
            total += x
            count += 1
    return total / count


def peak_memory_mb(function, *args):
    """Run function(*args) and report the most memory it used at once."""
    tracemalloc.start()
    result = function(*args)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return result, peak / 1_000_000


if __name__ == "__main__":
    write_fake_trajectory()
    print(f"trajectory: {N_FRAMES} frames x {N_ATOMS} atoms")

    answer, mb = peak_memory_mb(lambda: average_x(read_frames_as_list(FILE)))
    print(f"list:      average x = {answer:.4f}   peak memory {mb:7.2f} MB")

    answer, mb = peak_memory_mb(lambda: average_x(read_frames_one_at_a_time(FILE)))
    print(f"generator: average x = {answer:.4f}   peak memory {mb:7.2f} MB")
