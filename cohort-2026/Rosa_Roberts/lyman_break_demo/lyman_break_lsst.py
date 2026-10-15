"""
At what redshifts does the Ly-alpha break move through the LSST filters?

Loads the LSST total-throughput curves, builds a BAGPIPES model galaxy at
several redshifts (IGM absorption is applied by BAGPIPES), plots the SED over
the filters, and works out the redshift window where the Ly-alpha break sits
inside each band.

Outputs (written to ``--outdir``):
    sed_vs_redshift.png      One panel per redshift: model SED in f_nu with
                             the six LSST bands and the Ly-alpha break marked.
    lyman_break_windows.png  Horizontal bars showing the redshift range over
                             which the break falls inside each band.

Usage:
    python lyman_break_lsst.py
    python lyman_break_lsst.py --redshifts 3 4.5 6 --outdir figures/
"""

import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import bagpipes as pipes

plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})

matplotlib.use("Agg")  # no display in a container: save figures, don't show them


HERE = Path(__file__).resolve().parent
BANDS = "ugrizy"
COLOURS = dict(zip(BANDS, ["#7b3294", "#2c7bb6", "#1a9641", "#e08214", "#d7191c", "#8c510a"]))
LYA = 1215.67      # rest-frame Lyman-alpha, Angstrom
C_ANG = 2.998e18   # speed of light, Angstrom/s

DATA_DIR = HERE / "throughputs" / "baseline"
OUT_DIR = HERE / "output"

FILTER_HEIGHT = 0.6   # height of the TALLEST filter on the SED axis (others are in proportion)

# SED grid layout, all in figure fractions (0-1)
GRID = dict(left=0.10, right=0.98, bottom=0.10, top=0.88, wspace=0.05, hspace=0.25)
LEGEND_Y = 0.93       # bottom edge of the legend row: lower = closer to the panels
XLABEL_Y = 0.02       # bottom edge of the x label: higher = closer to the panels
YLABEL_X = 0.02       # left edge of the y label: higher = closer to the panels


def load_filter(band, data_dir=DATA_DIR):
    """Load the total-throughput curve for one LSST band.

    Reads ``total_<band>.dat`` from the LSST throughputs baseline, whose
    first column is wavelength in nm and second is total system throughput,
    and converts the wavelengths to Angstrom.

    Args:
        band: Single-letter LSST band name, one of "ugrizy".
        data_dir: Directory containing the ``total_<band>.dat`` files.

    Returns:
        Tuple ``(wavelength, throughput)`` of 1-D numpy arrays, with
        wavelength in Angstrom and throughput as a fraction (0-1).

    Raises:
        FileNotFoundError: If no throughput file exists for ``band``.
    """
    wav_nm, throughput = np.loadtxt(data_dir / f"total_{band}.dat", usecols=(0, 1), unpack=True)
    return wav_nm * 10.0, throughput


def band_edges(wav, throughput):
    """Find the blue and red edges of a filter.

    The edges are the shortest and longest wavelengths where the throughput
    is at least 1% of the filter's peak. This is wider than the half-maximum
    (FWHM) edges, so it includes the filter wings.

    Args:
        wav: 1-D array of wavelengths in Angstrom.
        throughput: 1-D array of throughput values, same length as ``wav``.

    Returns:
        Tuple ``(blue_edge, red_edge)`` in Angstrom.
    """
    inside = wav[throughput >= 0.01 * throughput.max()]
    return inside.min(), inside.max()


def make_model(z, wavs, *, exp_params=None):
    """Build a BAGPIPES model galaxy with an exponentially declining SFH.

    The default model is a young (100 Myr), low-metallicity (0.2 Z_sun)
    galaxy with 10^9 M_sun formed and light Calzetti dust (Av = 0.1).
    BAGPIPES applies IGM absorption for the given redshift, which is what
    produces the Ly-alpha break.

    Args:
        z: Redshift of the model galaxy.
        wavs: 1-D array of observed-frame wavelengths in Angstrom on which
            to compute the spectrum.
        exp_params: Optional dict of keys that override the defaults in the
            "exponential" component, e.g. ``{"age": 0.5, "tau": 1.0}``.
            Defaults to None, meaning no overrides. (None is used instead of
            ``{}`` because a mutable default would be shared between calls.)

    Returns:
        A ``bagpipes.model_galaxy``. Its ``.spectrum`` attribute is an
        (N, 2) array of wavelength (Angstrom) and f_lambda
        (erg/s/cm^2/Angstrom).
    """
    if exp_params is None:  # None instead of a mutable {} default
        exp_params = {}
    components = {
        "redshift": z,
        "t_bc": 0.01,
        "exponential": {"age": 0.1, "tau": 0.3, "massformed": 9.0, "metallicity": 0.2, **exp_params},
        "dust": {"type": "Calzetti", "Av": 0.1},
        # "nebular": {"logU": -2.5},
    }
    return pipes.model_galaxy(components, spec_wavs=wavs)


def f_nu(*, wavs, f_lambda):
    """Convert flux density per unit wavelength to per unit frequency.

    Uses f_nu = f_lambda * lambda^2 / c. Both arguments are keyword-only
    because they are arrays of the same shape, so swapping them by position
    would silently give the wrong answer instead of raising an error.

    Args:
        wavs: Wavelengths in Angstrom.
        f_lambda: Flux density in erg/s/cm^2/Angstrom, same shape as ``wavs``.

    Returns:
        Flux density in erg/s/cm^2/Hz, same shape as the inputs.
    """
    return f_lambda * wavs**2 / C_ANG


def break_windows(filters):
    """Work out the redshift range where the Ly-alpha break is inside each band.

    The break sits at an observed wavelength of LYA * (1 + z), so a filter
    edge at wavelength lambda corresponds to z = lambda / LYA - 1. Filter
    edges come from ``band_edges`` (1% of peak throughput).

    Args:
        filters: Dict mapping band name to a ``(wavelength, throughput)``
            tuple, as returned by ``load_filter``.

    Returns:
        Dict mapping band name to ``(z_low, z_high)``, the redshifts at
        which the break enters and leaves the band.
    """
    return {band: tuple(edge / LYA - 1 for edge in band_edges(*curve))
            for band, curve in filters.items()}


def plot_sed_panels(redshifts, filters, *, wavs, path):
    """Plot the model SED at each redshift over the LSST filter curves.

    Draws one panel per redshift on a two-column grid. Each panel shows the
    model f_nu, normalised to its median redward of the Ly-alpha break, with
    the filter curves shaded underneath (scaled so the tallest filter has
    height ``FILTER_HEIGHT``) and the break marked as a dashed line. Unused
    panels are hidden and the figure is saved rather than shown.

    Args:
        redshifts: Sequence of redshifts, one per panel.
        filters: Dict mapping band name to a ``(wavelength, throughput)``
            tuple, as returned by ``load_filter``.
        wavs: 1-D array of observed-frame wavelengths in Angstrom for the
            model spectra; also sets the x-axis range.
        path: File path to save the figure to (format taken from the
            extension).
    """
    ncols = 2
    nrows = int(np.ceil(len(redshifts) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(9, 3.6 * nrows + 0.6),
                             sharex=True, sharey=True, squeeze=False)
    tallest = max(ft.max() for _, ft in filters.values())  # one common scale for all bands
    for ax, z in zip(axes.flat, redshifts):
        flux = f_nu(wavs=wavs, f_lambda=make_model(z, wavs).spectrum[:, 1])
        flux = flux / np.median(flux[wavs > LYA * (1 + z)])  # normalise to flux redward of the break
        ax.plot(wavs, flux, color="k", lw=1.2)
        for band, (fw, ft) in filters.items():
            ax.fill_between(fw, 0, FILTER_HEIGHT * ft / tallest,
                            color=COLOURS[band], alpha=0.5, label=band)
        ax.axvline(LYA * (1 + z), color="grey", ls="--", lw=1.2, label=r"Ly$\alpha$ break")
        ax.set_title(f"z = {z:.1f}")
        ax.set_xlim(wavs.min(), wavs.max())
        ax.set_ylim(0, 1.5)
    for ax in axes.flat[len(redshifts):]:
        ax.set_visible(False)

    fig.subplots_adjust(**GRID)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, LEGEND_Y),
               ncol=len(labels), frameon=False)
    fig.supxlabel("Observed wavelength (Å)", fontsize=14,
                  x=(GRID["left"] + GRID["right"]) / 2, y=XLABEL_Y)
    fig.supylabel("Normalised $f_\\nu$ (filter heights ∝ throughput)", fontsize=14,
                  x=YLABEL_X, y=(GRID["bottom"] + GRID["top"]) / 2)
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_windows(windows, path):
    """Plot the Ly-alpha break redshift window for each band as horizontal bars.

    Bands are listed top to bottom in the order given (u at the top for
    "ugrizy") and each bar is coloured to match the SED figure.

    Args:
        windows: Dict mapping band name to ``(z_low, z_high)``, as returned
            by ``break_windows``.
        path: File path to save the figure to (format taken from the
            extension).
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (band, (z_lo, z_hi)) in enumerate(windows.items()):
        ax.barh(i, z_hi - z_lo, left=z_lo, color=COLOURS[band])
    ax.set_yticks(range(len(windows)), labels=list(windows))
    ax.invert_yaxis()
    ax.set_xlabel("Redshift at which the Ly$\\alpha$ break falls in the band")
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main():
    """Parse command-line arguments, print the break windows and save both figures."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--redshifts", type=float, nargs="+", default=[2, 3, 4, 5],
                        help="redshifts to plot, one SED panel each (default: 2 3 4 5)")
    parser.add_argument("--outdir", type=Path, default=OUT_DIR,
                        help="directory to save the figures in (default: ./output)")
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    filters = {band: load_filter(band) for band in BANDS}
    wavs = np.arange(3000.0, 12000.0, 10.0)

    windows = break_windows(filters)
    for band, (z_lo, z_hi) in windows.items():
        print(f"{band}: Lyman-alpha break inside band for z = {z_lo:.2f} to {z_hi:.2f}")

    sed_path = args.outdir / "sed_vs_redshift.png"
    windows_path = args.outdir / "lyman_break_windows.png"
    plot_windows(windows, windows_path)
    plot_sed_panels(args.redshifts, filters, wavs=wavs, path=sed_path)
    print(f"Saved {sed_path}\nSaved {windows_path}")


if __name__ == "__main__":
    main()



