"""Item 6: Prefer Multiple Assignment Unpacking Over Indexing.

Indexing into tuples (`row[0]`, `row[1]`) hides meaning; unpacking names
every field at the point of use and fails loudly if the shape changes.
"""

# Each record: (scenario, input heating power MW, (mean T keV, std T keV))
RUNS = [
    ("ohmic", 1.5, (2.48, 0.31)),
    ("nbi", 10.0, (8.05, 0.92)),
    ("ecrh", 6.0, (6.73, 0.66)),
]


def summarise_indexing(runs):
    """The hard-to-read version."""
    lines = []
    for i in range(len(runs)):
        run = runs[i]
        lines.append(f"{run[0]}: {run[2][0]:.2f} keV per {run[1]} MW")
    return lines


def summarise_unpacking(runs):
    """Same output, but every value has a name."""
    lines = []
    for scenario, power_mw, (mean_t, _std_t) in runs:
        lines.append(f"{scenario}: {mean_t:.2f} keV per {power_mw} MW")
    return lines


def bounds(samples):
    """Return (lowest, highest) of a sequence; callers unpack the pair."""
    ordered = sorted(samples)
    return ordered[0], ordered[-1]


def main():
    print("=== Item 6: Prefer unpacking over indexing ===")
    print("Indexing :", summarise_indexing(RUNS))
    print("Unpacking:", summarise_unpacking(RUNS))

    low, high = bounds([7.9, 8.4, 7.6, 8.1])
    print(f"\nUnpacking a returned tuple: low={low}, high={high}")

    # Swap without a temporary variable (handy in sorting / bisection code).
    a, b = 1.0, 2.0
    a, b = b, a
    print(f"Swap in one line: a={a}, b={b}")

    # Unpacking fails loudly if the data shape changes -- a feature, not a bug.
    try:
        scenario, power_mw = RUNS[0]
    except ValueError as err:
        print(f"Shape mismatch caught early: {err}")


if __name__ == "__main__":
    main()
