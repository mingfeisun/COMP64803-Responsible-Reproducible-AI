def generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = generator()
my_func(*it)