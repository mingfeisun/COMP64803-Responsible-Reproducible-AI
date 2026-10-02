def safe_divide(a, b):
    print("\nCalling safe_divide...")

    try:
        print("TRY: Attempting the division")
        result = a / b
    except ZeroDivisionError:
        print("EXCEPT: Caught a division-by-zero error")
        raise ValueError("ValueError: Zero Division!")
    else:
        print("ELSE: Division succeeded, using result")
        return result
    finally:
        print("FINALLY: This always runs (cleanup, logging, etc.)")


if __name__ == "__main__":

    print(safe_divide(10, 2))   # No exception
    print(safe_divide(10, 0))   # Exception raised