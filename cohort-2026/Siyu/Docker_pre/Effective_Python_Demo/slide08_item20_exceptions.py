# Item 20: Prefer Raising Exceptions to Returning None

def best_drag_none(values):
    if not values:
        return None
    return min(values)

print("Returning None:", best_drag_none([]))


def best_drag(values):
    if not values:
        raise ValueError("No observations")
    return min(values)

print("Valid result:", best_drag([0.012, 0.015, 0.018]))

try:
    best_drag([])
except ValueError:
    print("Invalid inputs")
