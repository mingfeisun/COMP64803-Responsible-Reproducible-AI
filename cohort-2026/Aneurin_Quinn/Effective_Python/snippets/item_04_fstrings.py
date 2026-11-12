"""Item 4: Prefer Interpolated F-Strings Over C-style Format Strings and str.format.

Logging simulation outputs is constant in research code. f-strings put the
value right next to its formatting, so they are shorter and harder to get
wrong than % or .format().
"""

# Mean and standard deviation of peak plasma temperature (keV)
# from a small Monte Carlo study, per heating scenario.
RESULTS = {"ohmic": (2.4813, 0.3127), "nbi": (8.0461, 0.9152), "ecrh": (6.7302, 0.6611)}


def c_style(name, mean, std):
    return "%-6s T = %.2f +/- %.2f keV" % (name, mean, std)


def format_method(name, mean, std):
    return "{:<6} T = {:.2f} +/- {:.2f} keV".format(name, mean, std)


def f_string(name, mean, std):
    return f"{name:<6} T = {mean:.2f} +/- {std:.2f} keV"


def relative_uncertainty(mean, std):
    # Expressions and format specs work inline: % formatting of a ratio.
    return f"{std / mean:.1%}"


def main():
    print("=== Item 4: Prefer f-strings ===")
    name, (mean, std) = "nbi", RESULTS["nbi"]
    print("C-style     :", c_style(name, mean, std))
    print("str.format  :", format_method(name, mean, std))
    print("f-string    :", f_string(name, mean, std))

    print("\nAll scenarios, with inline expressions:")
    for name, (mean, std) in RESULTS.items():
        print(f"  {f_string(name, mean, std)}  (rel. {relative_uncertainty(mean, std)})")

    # Python 3.8+: the '=' specifier is great for quick debugging.
    n_samples = 1000
    print(f"\nDebug print: {n_samples=}, {mean=:.3f}")


if __name__ == "__main__":
    main()
