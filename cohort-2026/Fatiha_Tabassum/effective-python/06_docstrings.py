
    
  
"""Analyse synthetic magnetic resonance measurements.

This module demonstrates module, class, and function docstrings for
Effective Python, Item 84. The measurements are illustrative, not
experimental data.
"""

from dataclasses import dataclass


@dataclass
class ResonanceMeasurement:
    """Represent one magnetic resonance measurement.

    Attributes:
        frequency_ghz: Measurement frequency in gigahertz.
        response: Normalised resonance signal (dimensionless).
    """

    frequency_ghz: float
    response: float


def lorentzian_response(frequency_ghz: float, centre_ghz: float, width_ghz: float) -> float:
    """Calculate a normalised Lorentzian resonance response.

    Args:
        frequency_ghz: Frequency at which to evaluate the response.
        centre_ghz: Resonance centre frequency.
        width_ghz: Positive half-width at half-maximum.

    Returns:
        The dimensionless response, between zero and one.

    Raises:
        ValueError: If ``width_ghz`` is not positive.
    """
    if width_ghz <= 0:
        raise ValueError("width_ghz must be positive")

    return 1.0 / (1.0 + ((frequency_ghz - centre_ghz) / width_ghz) ** 2)


def make_measurements(frequencies_ghz: list[float]) -> list[ResonanceMeasurement]:
    """Create synthetic measurements for a fixed resonance model.

    Args:
        frequencies_ghz: Frequencies to evaluate, in gigahertz.

    Returns:
        One ``ResonanceMeasurement`` per input frequency, in order.
    """
    return [
        ResonanceMeasurement(frequency, lorentzian_response(frequency, 5.0, 0.4))
        for frequency in frequencies_ghz
    ]


if __name__ == "__main__":
    print("Synthetic magnetic resonance measurements:")
    for measurement in make_measurements([4.5, 5.0, 5.5]):
        print(f"{measurement.frequency_ghz:.1f} GHz -> {measurement.response:.3f}")

    print("\nFunction documentation:")
    help(lorentzian_response)

