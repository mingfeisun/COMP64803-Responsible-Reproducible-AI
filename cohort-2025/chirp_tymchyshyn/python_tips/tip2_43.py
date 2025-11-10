def load_events(n):
    events = []
    for i in range(n):
        events.append({"id": i, "energy": i * 0.5})
    return events

def stream_events(n):
    for i in range(n):
        yield {"id": i, "energy": i * 0.5}

stream_events(1000000)
load_events(1000000)
