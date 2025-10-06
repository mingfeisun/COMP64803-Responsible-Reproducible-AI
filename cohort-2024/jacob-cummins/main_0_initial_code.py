import sys

sys.set_int_max_str_digits(10000000) 

def fibonacci_number_matcher(n: int, contains: int) -> list[int]:
    """
    Finds all the occurances of a number within numbers in the fibonacci sequence.

    Args:
        n (int): The number of places to consider the sequence to.
        contains (int): What number is being looked for.

    Returns:
        list[int]: The numbers found that contain the desired number.
    """
    sequence = fibonacci(n=n)

    fib_contains = list(filter(lambda x: str(contains) in str(x), sequence))
    
    return fib_contains

def fibonacci(n: int) -> list[int]:
    """
    Calculates the fibonacci sequence upto n places.

    Args:
        n (int): The number of places to consider the sequence to.

    Returns:
        list[int]: The fibonacci sequence up to n places.
    """
    sequence = []
    for i in range(n):
        if i == 0:
            sequence.append(0)
        elif i == 1:
            sequence.append(1)
        else:
            sequence.append(sequence[i-1]+sequence[i-2])
    
    return sequence

#print(fibonacci_number_matcher(n=30000, contains=666))

#out = fibonacci_number_matcher(n=30000, contains=666)

#print(out[0])
#out = fibonacci_number_matcher(n=100000, contains=3)
#out = fibonacci_number_matcher(n=10000, contains=666)
#out = fibonacci_number_matcher(n=30000, contains=666)

#print(out[0])