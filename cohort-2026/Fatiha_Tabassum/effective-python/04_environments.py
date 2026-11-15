"""Item 83: Show interpreter and dependency versions inside Docker."""

import platform
import sys

import numpy


if __name__ == "__main__":
    print("Python:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print("NumPy:", numpy.__version__)
    print("Sample array:", numpy.linspace(4.0, 6.0, 5))
