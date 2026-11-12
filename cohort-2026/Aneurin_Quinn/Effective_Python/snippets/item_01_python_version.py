"""Item 1: Know Which Version of Python You're Using.

Reproducibility starts with the interpreter. A UQ study that ran on
Python 3.9 and is re-run on 3.12 can change behaviour (new syntax, new
library wheels, different random-number defaults in dependencies), so
record the version and fail loudly if it is wrong.
"""

import platform
import sys

MIN_VERSION = (3, 10)  # match/case and zip(strict=True) need 3.10+


def check_python_version(minimum=MIN_VERSION):
    """Raise RuntimeError if the running interpreter is older than `minimum`."""
    if sys.version_info < minimum:
        wanted = ".".join(map(str, minimum))
        raise RuntimeError(
            f"Python {wanted}+ required, found {platform.python_version()}"
        )
    return sys.version_info[:3]


def environment_report():
    """Return a dict worth saving next to every set of simulation results."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "executable": sys.executable,
        "platform": platform.platform(),
    }


def main():
    print("=== Item 1: Know which version of Python you're using ===")
    print("From the shell:  python3 --version")
    print(f"sys.version      -> {sys.version.split()[0]}")
    print(f"sys.version_info -> {tuple(sys.version_info[:3])}")
    check_python_version()
    print(f"OK: interpreter satisfies >= {'.'.join(map(str, MIN_VERSION))}")
    print("\nEnvironment report (store this with your results):")
    for key, value in environment_report().items():
        print(f"  {key:<15}{value}")


if __name__ == "__main__":
    main()
