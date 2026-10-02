import sys
import warnings

try:
    import gmpy2
    gmpy2_available = True
except ImportError:
    gmpy2_available = False

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

    fib_contains = [number for number in sequence if str(contains) in str(number)]

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
    if gmpy2_available:
        for i in range(n):
            if i == 0:
                sequence.append(gmpy2.mpz(0))
            elif i == 1:
                sequence.append(gmpy2.mpz(1))
            else:
                sequence.append(sequence[i-1] + sequence[i-2])
    else:
        warnings.warn('In future releases gmpy2 will be required', DeprecationWarning)
        for i in range(n):
            if i == 0:
                sequence.append(0)
            elif i == 1:
                sequence.append(1)
            else:
                sequence.append(sequence[i-1]+sequence[i-2])
    
    return sequence


#out = fibonacci_number_matcher(n=100000, contains=3)
#out = fibonacci_number_matcher(n=10000, contains=666)
out = fibonacci_number_matcher(n=30000, contains=666)

print(out[0])

#print(fibonacci(10))
#print(fibonacci_number_matcher(n=10, contains=1))