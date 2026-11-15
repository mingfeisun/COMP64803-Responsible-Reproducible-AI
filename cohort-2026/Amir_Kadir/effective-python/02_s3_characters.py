
from itertools import permutations

# Check whether a tuple represents an element of S3
def is_s3(g):
    return (
        isinstance(g, tuple)
        and len(g) == 3
        and all(type(x) is int for x in g)
        and set(g) == {0, 1, 2}
    )


# BEFORE: Return None for invalid input
def character_before(g):
    if not is_s3(g):
        return None

    fixed_points = sum(g[i] == i for i in range(3))
    return fixed_points - 1


# AFTER: Raise an exception for invalid input
def character_after(g):
    if not is_s3(g):
        raise ValueError("Not an element of S3")

    fixed_points = sum(g[i] == i for i in range(3))
    return fixed_points - 1


# Compare character values for the three conjugacy classes
representatives = {
    "Identity": (0, 1, 2),
    "Transposition": (1, 0, 2),
    "3-cycle": (1, 2, 0),
}

for name, g in representatives.items():
    before = character_before(g)
    after = character_after(g)

    assert before == after
    print(f"{name}: Before = {before}, After = {after}")


# Verify agreement on every element of S3
for g in permutations(range(3)):
    assert character_before(g) == character_after(g)


# Compare how invalid inputs are handled
invalid = (0, 0, 2)

assert character_before(invalid) is None
print("Before (invalid input):", character_before(invalid))

try:
    character_after(invalid)
except ValueError as error:
    print("After (invalid input):", error)
else:
    raise AssertionError("Expected a ValueError")


print("All S3 character checks passed!")
