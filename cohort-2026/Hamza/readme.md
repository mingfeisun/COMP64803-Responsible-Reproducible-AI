# Five ways to write better Python

Hamza Eljabiri, COMP64803, cohort 2026.

Five short scripts, each running a slow and a fast version of the same task on the same data.

1. Sets for membership tests, `snippets/way1_sets.py`
2. Deques for queues, `snippets/way2_deque.py`
3. Generators for single-pass loops, `snippets/way3_generators.py`
4. Caching for repeated calls, `snippets/way4_cache.py`
5. Binary search on sorted lists, `snippets/way5_bisect.py`

`run_all.py` runs the five scripts, `tests/` checks that each fast version gives the same answer as
its slow version, `Dockerfile` builds the environment, `sample_output.txt` is one run, and `slides/`
holds the talk.
