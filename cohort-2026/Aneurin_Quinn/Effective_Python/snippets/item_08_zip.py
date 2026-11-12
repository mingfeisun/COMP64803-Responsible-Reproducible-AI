"""Item 8: Use zip to Process Iterators in Parallel.

Comparing model predictions against measurements means walking several
lists side by side. zip does that without index bookkeeping, and
strict=True (Python 3.10+) catches silently mismatched lengths.
"""

SENSORS = ["TC-01", "TC-02", "TC-03", "TC-04"]
MEASURED_K = [612.0, 640.5, 701.2, 688.9]   # thermocouple readings (K)
PREDICTED_K = [605.3, 652.1, 694.8, 690.2]  # surrogate model mean (K)
PRED_STD_K = [8.0, 5.0, 9.1, 4.0]           # surrogate model std (K)


def residuals_with_range(measured, predicted):
    out = []
    for i in range(len(measured)):
        out.append(measured[i] - predicted[i])
    return out


def residuals_with_zip(measured, predicted):
    return [m - p for m, p in zip(measured, predicted, strict=True)]


def outside_two_sigma(names, measured, predicted, std):
    """Sensors whose measurement falls outside the 95% predictive band."""
    return [
        name
        for name, m, p, s in zip(names, measured, predicted, std, strict=True)
        if abs(m - p) > 2 * s
    ]


def main():
    print("=== Item 8: Use zip to process iterators in parallel ===")
    print("range(len()):", residuals_with_range(MEASURED_K, PREDICTED_K))
    print("zip         :", [round(r, 1) for r in residuals_with_zip(MEASURED_K, PREDICTED_K)])

    print("\nSensor   meas    pred +/- std")
    for name, m, p, s in zip(SENSORS, MEASURED_K, PREDICTED_K, PRED_STD_K):
        print(f"{name:<7}{m:7.1f} {p:7.1f} +/- {s:.1f}")

    print("\nOutside 2-sigma band:", outside_two_sigma(SENSORS, MEASURED_K, PREDICTED_K, PRED_STD_K))

    # Pitfall: plain zip silently truncates to the shortest input.
    short = PREDICTED_K[:3]
    print(f"\nPlain zip with a missing prediction -> {len(list(zip(MEASURED_K, short)))} pairs (silent!)")
    try:
        residuals_with_zip(MEASURED_K, short)
    except ValueError as err:
        print(f"zip(strict=True) -> ValueError: {err}")


if __name__ == "__main__":
    main()
