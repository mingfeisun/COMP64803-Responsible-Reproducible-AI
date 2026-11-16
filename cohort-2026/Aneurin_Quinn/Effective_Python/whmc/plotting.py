"""Publication-quality convergence plot.

Good figures: high resolution (300 dpi PNG for slides) plus a vector SVG
that stays sharp at any zoom, labelled axes, and log scales when the
errors span several orders of magnitude.
"""

import matplotlib

matplotlib.use("Agg")  # no screen needed (e.g. inside Docker)

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


def plot_convergence(steps, whmc_err, grid_err, path, *, dpi=300):
    """Save |pricing error| vs time steps as <path>.png (at dpi) and <path>.svg.

    Returns the list of files written.
    """
    steps = np.asarray(steps, dtype=float)
    fig, ax = plt.subplots(figsize=(6.4, 4.4), constrained_layout=True)
    ax.loglog(steps, np.abs(grid_err), "o-", color="#D63E50", lw=2, label="Grid Monte Carlo")
    ax.loglog(steps, np.abs(whmc_err), "s-", color="#1F9E72", lw=2, label="Wiener–Hopf Monte Carlo")
    ax.set_xlabel("time steps n")
    ax.set_ylabel("|price error| vs exact closed form")
    ax.set_xticks(steps, [f"{int(s)}" for s in steps])
    ax.minorticks_off()
    ax.grid(True, which="major", color="0.9")
    fig.legend(loc="outside lower center", ncols=2, frameon=False, fontsize=9)
    ax.set_title("Up-and-out call: error vs number of steps")

    path.parent.mkdir(parents=True, exist_ok=True)
    written = [path.with_suffix(".png"), path.with_suffix(".svg")]
    fig.savefig(written[0], dpi=dpi)   # raster, for slides
    fig.savefig(written[1])            # vector, sharp at any size
    plt.close(fig)
    return written
