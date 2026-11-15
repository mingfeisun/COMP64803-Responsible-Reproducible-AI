
from itertools import permutations
from collections import defaultdict, Counter
from math import factorial


# Compute the cycle type of a permutation
def cycle_type(p):
    visited = set()
    lengths = []

    for start in range(len(p)):
        if start in visited:
            continue

        current = start
        length = 0

        while current not in visited:
            visited.add(current)
            current = p[current]
            length += 1

        lengths.append(length)

    return tuple(sorted(lengths, reverse=True))


# BEFORE: Manual enumeration and dictionary counting
counts_before = {}

for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                sigma = (a, b, c, d)

                if len(set(sigma)) == 4:
                    typ = cycle_type(sigma)

                    counts_before.setdefault(typ, 0)
                    counts_before[typ] += 1


# AFTER: Item 36 (itertools) + Item 17 (defaultdict)
counts_after = defaultdict(int)

for sigma in permutations(range(4)):
    counts_after[cycle_type(sigma)] += 1


# Supporting Item 27: Mathematical set comprehensions

# BEFORE: map and set
types_before = set(
    map(cycle_type, permutations(range(4)))
)

# AFTER: set comprehension
types_after = {
    cycle_type(sigma)
    for sigma in permutations(range(4))
}


# Verify the before and after implementations
assert counts_before == counts_after
assert types_before == types_after
assert types_after == set(counts_after)


# Independent mathematical check using the class-size formula
def class_size_formula(partition):
    multiplicities = Counter(partition)

    z = 1
    for length, count in multiplicities.items():
        z *= length**count * factorial(count)

    return factorial(sum(partition)) // z


print("Conjugacy classes of S4:")

for typ in sorted(counts_after, reverse=True):
    count = counts_after[typ]
    expected = class_size_formula(typ)

    assert count == expected

    print(
        f"Cycle type {typ}: "
        f"Before = {counts_before[typ]}, "
        f"After = {count}, "
        f"Formula = {expected}"
    )


assert sum(counts_after.values()) == factorial(4)
assert len(counts_after) == 5

print("Distinct cycle types:", types_after)
print("All S4 conjugacy class checks passed!")
