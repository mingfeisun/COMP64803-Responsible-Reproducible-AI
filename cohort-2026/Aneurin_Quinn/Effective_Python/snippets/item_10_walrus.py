"""Item 10: Prevent Repetition with Assignment Expressions (the walrus :=).

Iterative solvers and sampling loops often compute a value, test it, and
then use it. `:=` assigns and tests in one place, removing duplicated
calls and awkward `while True: ... break` loops.
"""

import random


def relative_change(new, old):
    return abs(new - old) / abs(old)


def fixed_point_without_walrus(f, x0, tol=1e-8, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_new = f(x)
        change = relative_change(x_new, x)
        x = x_new
        if change < tol:
            return x, i + 1
    raise RuntimeError("did not converge")


def fixed_point_with_walrus(f, x0, tol=1e-8, max_iter=100):
    x = x0
    for i in range(max_iter):
        if relative_change(x_new := f(x), x) < tol:
            return x_new, i + 1
        x = x_new
    raise RuntimeError("did not converge")


def accepted_samples(n, threshold, seed=0):
    """Keep squared Gaussian draws below `threshold`, computing each square once."""
    rng = random.Random(seed)
    draws = (rng.gauss(0.0, 1.0) for _ in range(n))
    return [y for x in draws if (y := x * x) < threshold]


def main():
    print("=== Item 10: Prevent repetition with := ===")
    # Toy equilibrium: x = cos(x) (stands in for a coupled-physics iteration).
    import math

    print("Without walrus:", fixed_point_without_walrus(math.cos, 1.0))
    print("With walrus   :", fixed_point_with_walrus(math.cos, 1.0))

    kept = accepted_samples(1000, threshold=1.0)
    print(f"\nKept {len(kept)} / 1000 squared draws below 1 (each square computed once)")

    # Reading a stream until it is exhausted -- no 'while True' + break needed.
    chunks = iter(["chunk-1", "chunk-2", "chunk-3"])
    while (chunk := next(chunks, None)) is not None:
        print(f"processing {chunk}")


if __name__ == "__main__":
    main()
