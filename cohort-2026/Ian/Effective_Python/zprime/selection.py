"""Deciding which events to keep ("cuts")."""

CUTS = {"tau_pt_min": 30.0, "abs_eta_max": 2.5, "n_bjets_min": 1}


def passes(event, *, tau_pt_min, abs_eta_max, n_bjets_min):
    """True if the event survives every cut.

    Item 25: the `*` forces callers to name each cut, so two numbers can
    never be swapped by accident.
    Item 8: zip walks the two per-tau lists side by side.
    """
    for pt, eta in zip(event["tau_pt"], event["tau_eta"], strict=True):
        if pt < tau_pt_min or abs(eta) > abs_eta_max:
            return False
    return event["n_bjets"] >= n_bjets_min


def select(events, **cuts):
    """Item 27: a list comprehension instead of filter + lambda."""
    return [event for event in events if passes(event, **cuts)]
