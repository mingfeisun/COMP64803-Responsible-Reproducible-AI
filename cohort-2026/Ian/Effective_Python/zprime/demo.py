"""Run the demos:  python -m zprime.demo [item4|item7|item8|item27|item25|cutflow|all]"""
import sys

from zprime.cutflow import cutflow, format_cutflow
from zprime.events import make_events
from zprime.selection import CUTS, passes, select

EVENTS = make_events(100_000)


def banner(title):
    print(f"\n=== {title} " + "=" * max(0, 60 - len(title)))


def item4():
    banner("Item 4: f-strings over % formatting")
    name, count, total = "at least 1 b-jet", 12345, 100000
    old = "%-18s%9d%7.1f%%" % (name, count, 100.0 * count / total)
    new = f"{name:<18}{count:>9,}{count / total:>8.1%}"
    print("C-style :", old)
    print("f-string:", new)


def item7():
    banner("Item 7: enumerate over range(len(...))")
    rows = cutflow(EVENTS)
    print("range(len(rows)) and indexing:")
    for i in range(len(rows)):
        print(f"  {i + 1}. {rows[i][0]}")
    print("enumerate(rows, 1):")
    for number, (name, _) in enumerate(rows, 1):
        print(f"  {number}. {name}")


def item8():
    banner("Item 8: zip to walk two lists together")
    event = EVENTS[0]
    for pt, eta in zip(event["tau_pt"], event["tau_eta"]):
        print(f"  tau with pT = {pt:5.1f} GeV at eta = {eta:+.2f}")
    broken = {"tau_pt": [50.0, 40.0], "tau_eta": [0.5]}      # one eta missing
    pairs = list(zip(broken["tau_pt"], broken["tau_eta"]))
    print(f"lists of length 2 and 1: zip quietly gives {len(pairs)} pair")
    try:
        list(zip(broken["tau_pt"], broken["tau_eta"], strict=True))
    except ValueError as err:
        print(f"zip(..., strict=True): ValueError: {err}")


def item27():
    banner("Item 27: comprehensions over map and filter")
    # One input feature for the classifier: the larger tau pT in each event.
    old = list(map(lambda e: max(e["tau_pt"]),
                   filter(lambda e: passes(e, **CUTS), EVENTS)))
    new = [max(e["tau_pt"]) for e in EVENTS if passes(e, **CUTS)]
    print(f"map + filter + lambda: {len(old)} values")
    print(f"list comprehension   : {len(new)} values, identical: {old == new}")


def item25():
    banner("Item 25: keyword-only arguments")
    event = EVENTS[0]
    print("named cuts     :", passes(event, tau_pt_min=30.0, abs_eta_max=2.5,
                                     n_bjets_min=1))
    try:
        passes(event, 2.5, 30.0, 1)                # pT and eta swapped!
    except TypeError as err:
        print(f"positional cuts: TypeError: {err}")


def show_cutflow():
    banner("The result: a cutflow table")
    print(format_cutflow(cutflow(EVENTS)))
    print(f"{len(select(EVENTS, **CUTS)):,} events kept as training data. "
          "Made-up data, not a physics result.")


DEMOS = {"item4": item4, "item7": item7, "item8": item8, "item27": item27,
         "item25": item25, "cutflow": show_cutflow}

if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else "all"
    if choice != "all" and choice not in DEMOS:
        sys.exit(__doc__)
    # Item 1: know which version of Python you're using.
    print(f"Python {sys.version.split()[0]}")
    for name, demo in DEMOS.items():
        if choice in ("all", name):
            demo()
