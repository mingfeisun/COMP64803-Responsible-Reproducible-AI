"""Made-up collision events.

One "event" is one proton-proton collision, stored as a small record:

    {"tau_pt": [61.2, 34.9], "tau_eta": [0.41, -1.87], "n_bjets": 1}

    tau_pt   how hard each of the two tau particles was thrown out (GeV)
    tau_eta  the angle each tau came out at (0 = sideways, big = along the beam)
    n_bjets  how many "b-jets" were seen (a sign that top quarks were made)

The numbers are random. A fixed seed makes every run identical.
"""
import random


def make_events(n, seed=0):
    rng = random.Random(seed)
    events = []
    for _ in range(n):
        events.append({
            "tau_pt": [round(rng.expovariate(1 / 40), 1) for _ in range(2)],
            "tau_eta": [round(rng.uniform(-3.0, 3.0), 2) for _ in range(2)],
            "n_bjets": rng.choice([0, 0, 1, 1, 2]),
        })
    return events
