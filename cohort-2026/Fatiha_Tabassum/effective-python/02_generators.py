"""Item 30: Stream synthetic measurements rather than returning a list."""

from itertools import islice
from sys import getsizeof


def measurement_list(count):
    return [(i, 1.0 / (1.0 + ((i * 0.001 - 5) / 0.4) ** 2))
            for i in range(count)]


def measurement_generator(count):
    for i in range(count):
        yield i, 1.0 / (1.0 + ((i * 0.001 - 5) / 0.4) ** 2)


if __name__ == "__main__":
    count = 100_000
    values = measurement_list(count)
    stream = measurement_generator(count)
    print("List container size (excludes elements):", getsizeof(values), "bytes")
    print("Generator object size:", getsizeof(stream), "bytes")
    print("First three streamed measurements:", list(islice(stream, 3)))
