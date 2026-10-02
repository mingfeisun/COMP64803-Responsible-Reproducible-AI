# Consider generator functions instead of building big lists

# list
def list_countdown(n):
    return [i for i in reversed(range(n))]

print(list_countdown(5))

# generator
def gen_countdown(n):
    for i in reversed(range(n)):
        print(f"{i}...")
        yield i


it = gen_countdown(5)
next(it)
next(it)
next(it)


