# Effective Python: AI-Guided Spintronics Examples

**Module:** COMP64803 — Introduction to Responsible & Reproducible AI

This project contains five teaching demonstrations inspired by Brett Slatkin's *Effective Python (2nd edition)*, with an additional example exploring parallel processing.

The examples use synthetic magnetic resonance measurements to illustrate good Python programming practices relevant to scientific computing, machine learning, and AI-guided spintronics.

**Note:** The Lorentzian resonance function is illustrative and does not represent a complete physical model of a spintronic device.

## 1. Topics Covered

| Item | Topic | Python Script |
|---|---|---|
| 2 | Follow the PEP 8 Style Guide | `01_pep8.py` |
| 30 | Consider Generators Instead of Returning Lists | `02_generators.py` |
| 70 | Profile Before Optimising | `03_profiling.py` |
| 83 | Use Virtual Environments for Isolated and Reproducible Dependencies | `04_environments.py` |
| 84 | Write Docstrings for Every Function, Class, and Module | `06_docstrings.py` |
| 64 (Additional) | Consider `concurrent.futures` for True Parallelism | `05_parallelism.py` |

## 2. Build and Run in Docker

The demonstrations are packaged in Docker to provide a consistent Python environment.

### Build the Docker image

```bash
docker build -t effective-python-demo .
```

### Run the five presentation examples

**Item 2 — PEP 8**

```bash
docker run --rm effective-python-demo python 01_pep8.py
```

**Item 30 — Generators**

```bash
docker run --rm effective-python-demo python 02_generators.py
```

**Item 70 — Profiling**

```bash
docker run --rm effective-python-demo python 03_profiling.py
```

**Item 83 — Reproducible Environments**

```bash
docker run --rm effective-python-demo python 04_environments.py
```

**Item 84 — Docstrings**

```bash
docker run --rm effective-python-demo python 06_docstrings.py
```

### Additional example — Parallelism

```bash
docker run --rm --cpus=2 effective-python-demo python 05_parallelism.py
```

## 3. Demonstrations and Results

### Item 2 — Follow the PEP 8 Style Guide

PEP 8 provides conventions for writing readable and consistent Python code.

Key recommendations include:

- Use four spaces for indentation rather than tabs.
- Keep lines within the recommended length.
- Use descriptive `snake_case` names for functions and variables.
- Organise imports consistently.
- Write clear expressions and statements.

The example calculates a normalised Lorentzian resonance response.

**Output:**

```text
f=4.5 GHz, response=0.390
f=5.0 GHz, response=1.000
f=5.5 GHz, response=0.390
```

### Item 30 — Consider Generators Instead of Returning Lists

Generators produce values lazily using the `yield` keyword rather than storing every result in memory.

They are particularly useful for processing large datasets or streaming measurements.

**Measured results:**

```text
List container size (excludes elements): 800984 bytes
Generator object size: 224 bytes
```

The generator object is substantially smaller than the list container.

However, `sys.getsizeof()` measures shallow object sizes rather than total memory consumption. The generator also produces values on demand, whereas the list has already stored its elements.

### Item 70 — Profile Before Optimising

Python's built-in `cProfile` module identifies where a program spends its execution time.

The example profiles a simulated frequency sweep and identifies repeated function calls.

**Profiling result:**

```text
100000 calls to lorentzian()
```

**Execution times:**

```text
slow: 0.0294 seconds
improved: 0.0265 seconds
```

The improved implementation was approximately 10% faster in this run.

Execution times vary between runs and machines. Reliable performance comparisons require repeated measurements.

### Item 83 — Use Virtual Environments for Isolated and Reproducible Dependencies

Python virtual environments isolate project dependencies and help prevent package-version conflicts.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Record installed dependencies:

```bash
python3 -m pip freeze
```

Deactivate the environment:

```bash
deactivate
```

**Docker demonstration results:**

```text
Python: 3.12.16
NumPy: 2.2.6
Sample array: [4.  4.5 5.  5.5 6. ]
```

Docker and Python virtual environments provide different levels of isolation.

- A Python virtual environment isolates Python packages.
- Docker packages the Python runtime, dependencies, and system environment.

The Dockerfile specifies a Python base-image tag, and `requirements.txt` pins NumPy to version `2.2.6`.

For stronger reproducibility, pin the Docker image digest, lock transitive dependencies, and record relevant random seeds and hardware information.

### Item 84 — Write Docstrings for Every Function, Class, and Module

Docstrings explain the purpose and usage of Python modules, classes, functions, and methods.

A function docstring should describe:

- The purpose of the function.
- Its arguments.
- Its return values.
- Any exceptions it may raise.

The example documents a Lorentzian resonance function and uses Python's built-in `help()` function to display its documentation.

**Output:**

```text
Synthetic magnetic resonance measurements:
4.5 GHz -> 0.390
5.0 GHz -> 1.000
5.5 GHz -> 0.390
```

The `help()` function displays the function signature and documentation, including its arguments, return value, and possible `ValueError`.

Docstrings improve maintainability, collaboration, and code reuse in scientific research.

## 4. Additional Example: Parallel Processing

Item 64 demonstrates how `concurrent.futures.ProcessPoolExecutor` can distribute independent CPU-bound calculations across multiple processes.

**Measured results:**

```text
Sequential: 1.030 s
2 processes: 0.593 s
```

This corresponds to approximately **1.74× speedup** in the measured run.

Parallel processing introduces overhead, so performance improvements depend on workload size and available CPU resources.

## 5. Key Takeaways

Writing better scientific Python involves more than producing correct numerical results.

The five practices demonstrate how to:

1. Improve readability through consistent coding conventions.
2. Reduce unnecessary memory usage with generators.
3. Identify performance bottlenecks using profiling.
4. Manage dependencies for reproducible research.
5. Document code to support collaboration and reuse.

Together, these practices support more maintainable, efficient, and reproducible scientific software.

## Reference

Slatkin, B. *Effective Python: 90 Specific Ways to Write Better Python*. 2nd edition. Addison-Wesley, 2019.
