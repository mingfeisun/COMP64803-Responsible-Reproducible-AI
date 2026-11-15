
from sympy import Matrix, zeros

# Standard generators of sl_2
H = Matrix([[1, 0], [0, -1]])
E = Matrix([[0, 1], [0, 0]])
F = Matrix([[0, 0], [1, 0]])

A, B, C = H, E, F

# BEFORE: Expanded matrix calculations
BC = B @ C - C @ B
CA = C @ A - A @ C
AB = A @ B - B @ A

J_before = (
    A @ BC - BC @ A
    + B @ CA - CA @ B
    + C @ AB - AB @ C
)

# AFTER: Helper functions
def bracket(A, B):
    return A @ B - B @ A

def jacobi(A, B, C):
    return (
        bracket(A, bracket(B, C))
        + bracket(B, bracket(C, A))
        + bracket(C, bracket(A, B))
    )

J_after = jacobi(H, E, F)

# Verify both implementations
assert J_before == J_after
assert J_after == zeros(2, 2)

# Check the sl_2 commutation relations
assert bracket(H, E) == 2 * E
assert bracket(H, F) == -2 * F
assert bracket(E, F) == H

print("Before (expanded):", J_before)
print("After (helper functions):", J_after)
print("All Lie algebra checks passed!")
