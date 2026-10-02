# Combine multiple generators with yield from

# Functions that we want to do stuff with:
def produce_numbers():
    for i in range(10):
        yield i       

def double(stream):
    for x in stream:
        yield x * 2

def minus_one(stream):
    for x in stream:
        yield x - 1


# manual method appending lists
def pipeline_manual_append():
    out = []
    for a in produce_numbers():
        for b in double([a]):  
            for c in minus_one([b]):
                out.append(c)
    return out 


# manual method yield
def pipeline_manual_yield():
    for a in produce_numbers():
        for b in double([a]):  
            for c in minus_one([b]):
                yield c


# nice clean yield from
def pipeline():
    stage1 = produce_numbers()
    stage2 = double(stage1)
    stage3 = minus_one(stage2)

    yield from stage3



print("Manual append:   ", list(pipeline_manual_append()))
print("Manual yield:    ", list(pipeline_manual_yield()))
print("Yield-from:      ", list(pipeline()))
    