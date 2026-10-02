"""
Demonstration of poor vs. good PEP8 style.

"""

# BAD:

def bad(a,b):print("Total:",a+b)    # <-- missing spaces, one-line compound statement
                                    # no whitespace around +.

VERYlongVariableNameInteger=  12    # <-- confusing variable name style, spaces

x=10;y=10                           # <-- multiple inline statements, missing whitespace

def calc(x, y):return(x+y)/2

bad(x,y)
print(calc(VERYlongVariableNameInteger,5)) 

class badclassname:
    def __init__(self):    
        print("My name should be capitalised :(")       # should have blank lines
        pass
        from x import y                                 # put imports at the top of file     

# GOOD:

def add_numbers(left: int, right: int) -> int:
    """
    Return the sum of two integers.
    """
    return left + right


def compute_average(values: list[int]) -> float:
    """
    Compute the average of a list of integers.
    """
    return sum(values) / len(values)


def print_total(value: int) -> None:
    """
    Print a formatted message showing the total.
    """
    print(f"Total: {value}")


def main():
    """
    Demonstrates clean variable naming, spacing, and function calls.
    """
    number_list = [1, 2, 3] 
    x_value = 10                  
    y_value = 20

    total = add_numbers(x_value, y_value)
    avg = compute_average(number_list)

    print_total(total)
    print(f"Average: {avg}")


if __name__ == "__main__":  # module-entry pattern
    main()

