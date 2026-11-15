
# Effective Python for Mathematical Research

COMP64803 — Introduction to Responsible & Reproducible AI

## Overview

Five techniques from Brett Slatkin's *Effective Python*
(Second Edition), demonstrated using examples from
Lie algebras and representation theory.

Each example compares two correct Python implementations
and explains the improvement.

## Techniques

1. **Item 5 — Helper Functions (p. 21)**
   - Lie brackets and Jacobi identity in sl(2).
   - Improvement: Readability and mathematical abstraction.

2. **Item 20 — Exceptions (p. 80)**
   - Character of the standard representation of S3.
   - Improvement: Explicit failure handling and robustness.

3. **Item 36 — itertools (p. 138)**
   - Conjugacy classes of S4.
   - Supporting Items 17 (defaultdict) and 27
     (set comprehensions).
   - Improvement: Pythonic combinatorial computation.

4. **Item 30 — Generators (p. 114)**
   - Standard Young tableaux.
   - Improvement: Lazy evaluation and memory efficiency.

5. **Item 70 — Profiling (p. 322)**
   - Weight multiplicities in tensor powers of the
     standard sl(2) representation.
   - Supporting Item 81: Memory profiling with tracemalloc.
   - Improvement: Evidence-based optimisation.

**Supporting Item 76:** Automated testing across all five examples.

## Requirements

- Docker
- Python 3.12 (provided by Docker)
- SymPy 1.13.3 (installed inside Docker)

No local Python installation is required.

## Running the Demonstrations

Build the Docker image from this directory:

    docker build -t comp64803-effective-python .

Run each demonstration:

    docker run --rm comp64803-effective-python python 01_lie_brackets.py
    docker run --rm comp64803-effective-python python 02_s3_characters.py
    docker run --rm comp64803-effective-python python 03_symmetric_groups.py
    docker run --rm comp64803-effective-python python 04_young_tableaux.py
    docker run --rm comp64803-effective-python python 05_profiling.py

## Automated Tests

Run all five demonstration tests:

    docker run --rm comp64803-effective-python python -m unittest -v

The tests execute each demonstration, check the expected
outputs, and verify successful completion.

## Profiling Results

The examples use cProfile to investigate execution time
and tracemalloc to measure Python memory allocations.

For the task of retrieving the first standard Young tableau
of shape (10, 10), our Docker run measured:

- Eager list: 10,087,752 bytes peak traced memory
- Lazy generator: 25,496 bytes peak traced memory
- Reduction factor: 395.66x

These measurements are workload- and environment-specific.

## Reference

Brett Slatkin, Effective Python: 90 Specific Ways to
Write Better Python, Second Edition, Addison-Wesley.
