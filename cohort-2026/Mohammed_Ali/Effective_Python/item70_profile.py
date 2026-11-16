"""Item 70: Profile before optimizing.

An analysis loop does three jobs per frame: make the atoms, count
neighbours, and summarise. cProfile shows which one is actually slow,
so we only speed up that one, and check the answer hasn't changed.

Run: python item70_profile.py
"""
import cProfile
import pstats
import random
import time

from scipy.spatial import cKDTree

CUTOFF = 0.1
N_FRAMES = 10
N_ATOMS = 800


def load_atoms(seed):
    rng = random.Random(seed)
    return [(rng.random(), rng.random(), rng.random()) for _ in range(N_ATOMS)]


def count_neighbours_slow(atoms):
    """Every pair, with plain Python loops."""
    count = 0
    for i in range(len(atoms)):
        xi, yi, zi = atoms[i]
        for j in range(i + 1, len(atoms)):
            xj, yj, zj = atoms[j]
            if (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2 < CUTOFF**2:
                count += 1
    return count


def count_neighbours_fast(atoms):
    """A KD-tree (from SciPy) sorts atoms by position, so it only checks
    atoms that are already close, instead of every possible pair."""
    tree = cKDTree(atoms)
    return len(tree.query_pairs(CUTOFF))


def summarise(atoms):
    xs = [x for x, y, z in atoms]
    return sum(xs) / len(xs)


def analyse(count_function):
    total = 0
    for frame in range(N_FRAMES):
        atoms = load_atoms(frame)
        total += count_function(atoms)
        summarise(atoms)
    return total


if __name__ == "__main__":
    # 1. Profile: where does the time go?
    profiler = cProfile.Profile()
    profiler.runcall(analyse, count_neighbours_slow)
    print("Profile of the slow version (top 5 by total time):")
    pstats.Stats(profiler).strip_dirs().sort_stats("cumulative").print_stats(5)

    # 2. Fix only the slow part, and check the answer is the same.
    for function in (count_neighbours_slow, count_neighbours_fast):
        start = time.time()
        total = analyse(function)
        print(f"{function.__name__:<22} {time.time() - start:6.3f} s   ({total} neighbours)")
