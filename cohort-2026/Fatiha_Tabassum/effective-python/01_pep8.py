"""Item 2: Readable, consistently formatted scientific Python."""


def resonance_response(frequency, centre=5.0, width=0.4):
    """Return a unit-height Lorentzian response (GHz inputs)."""
    return 1.0 / (1.0 + ((frequency - centre) / width) ** 2)


if __name__ == "__main__":
    for frequency in (4.5, 5.0, 5.5):
        print(f"f={frequency:.1f} GHz, response={resonance_response(frequency):.3f}")
