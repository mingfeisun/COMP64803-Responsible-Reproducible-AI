import sys

# Generator function to yield even numbers up to n
def even_numbers_generator(n):
    for x in range(n):
        if x % 2 == 0:
            yield x

# List function to return all even numbers up to n in a list
def even_numbers_list(n):
    return [x for x in range(n) if x % 2 == 0]

# Using the generator
numbers_gen = even_numbers_generator(10**6)

print("Memory used by generator:", sys.getsizeof(numbers_gen), "bytes")

# Using the list function
numbers = even_numbers_list(10**6)

print("Memory used by list:", sys.getsizeof(numbers), "bytes")
