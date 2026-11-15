"""Item 1: Know Which Version of Python You're Using.

Book: `python` on the command line may not be the Python you think it is
(on older systems it was Python 2), so check with `python3 --version` or
`sys.version_info` at runtime.

ML angle: PyTorch / JAX wheels only exist for certain Python versions, and
a result you cannot re-run is not reproducible. So: check the version,
fail early if it is wrong, and save it with every experiment, next to the
random seed.
"""

import importlib.metadata
import json
import platform
import sys

MIN_VERSION = (3, 10)  # this repo uses zip(strict=True), added in 3.10


def check_python_version(minimum=MIN_VERSION):
    """Raise RuntimeError if the running interpreter is older than `minimum`."""
    if sys.version_info < minimum:
        wanted = ".".join(map(str, minimum))
        raise RuntimeError(
            f"Python {wanted}+ required, found {platform.python_version()}"
        )
    return sys.version_info[:3]


def package_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def run_metadata(seed, packages=("numpy", "torch", "jax", "pytest")):
    """Everything needed to say *how* a training run was produced."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "packages": {name: package_version(name) for name in packages},
        "seed": seed,
    }


def main():
    print("=== Item 1: Know which version of Python you're using ===")
    print("Shell:  python --version   (may be Python 2 on old systems!)")
    print("        python3 --version")
    print(f"sys.version_info -> {tuple(sys.version_info[:3])}")
    check_python_version()
    print(f"OK: interpreter satisfies >= {'.'.join(map(str, MIN_VERSION))}")
    print("\nSave this next to your checkpoints / results:")
    print(json.dumps(run_metadata(seed=42), indent=2))


if __name__ == "__main__":
    main()
