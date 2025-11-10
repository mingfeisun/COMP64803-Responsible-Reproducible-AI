# def infer_signal(event):
#     if "energy" not in event:
#         return None
#     return event["energy"] > 50

# result = infer_signal({})
# if result:
#     print("Signal detected!")  # never runs, no error seen
    
    
def infer_signal(event):
    if "energy" not in event:
        raise ValueError("missing 'energy' key in event data")
    return event["energy"] > 50

try:
    infer_signal({})
except ValueError as e:
    print("Error:", e)
