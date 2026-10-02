def sum_twice(l):
    total = 0
    for i in l:
        total += i
    for i in l:
        total += i
    return total

def safe_sum_twice(l):
    if iter(l) is l:
        raise TypeError("Must supply a container.")
    
    total = 0
    for i in l:
        total += i
    for i in l:
        total += i
    return total

def numbers_below(x):
    for i in range(x):
        yield i

class NumbersBelow:
    def __init__(self, x):
        self.x = x

    def __iter__(self):
        for i in range(self.x):
            yield i

it = numbers_below(2)
l = [0, 1]
c = NumbersBelow(2)

print(f"sum_twice(it): {sum_twice(it)}")
print(f"sum_twice(l): {sum_twice(l)}")
print(f"sum_twice(c): {sum_twice(c)}")

try:
    print(f"safe_sum_twice(it): {safe_sum_twice(it)}")
except TypeError:
    print("safe_sum_twice(it) raised a TypeError.")

try:
    print(f"safe_sum_twice(l): {safe_sum_twice(l)}")
except TypeError:
    print("safe_sum_twice(l) raised a TypeError.")

try:
    print(f"safe_sum_twice(c): {safe_sum_twice(c)}")
except TypeError:
    print("safe_sum_twice(c) raised a TypeError.")
