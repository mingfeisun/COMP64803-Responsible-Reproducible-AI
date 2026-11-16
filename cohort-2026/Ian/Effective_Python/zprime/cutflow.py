"""A cutflow: how many events are left after each cut is switched on."""
from zprime.selection import CUTS, select

NO_CUTS = {"tau_pt_min": 0.0, "abs_eta_max": 99.0, "n_bjets_min": 0}
STEPS = [
    ("all events", {}),
    ("tau pT > 30 GeV", {"tau_pt_min": CUTS["tau_pt_min"]}),
    ("tau |eta| < 2.5", {"abs_eta_max": CUTS["abs_eta_max"]}),
    ("at least 1 b-jet", {"n_bjets_min": CUTS["n_bjets_min"]}),
]


def cutflow(events):
    """Return [(step name, events left)], adding one cut at a time."""
    rows = []
    cuts = dict(NO_CUTS)
    for name, change in STEPS:
        cuts.update(change)
        rows.append((name, len(select(events, **cuts))))
    return rows


def format_cutflow(rows):
    """Item 7 (enumerate) numbers the rows; Item 4 (f-strings) lines them up."""
    total = rows[0][1]
    lines = [f"{'#':>2}  {'cut':<18}{'events':>9}{'kept':>8}"]
    for number, (name, count) in enumerate(rows, 1):
        lines.append(f"{number:>2}  {name:<18}{count:>9,}{count / total:>8.1%}")
    return "\n".join(lines)
