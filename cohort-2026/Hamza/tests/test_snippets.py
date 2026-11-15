"""Each test checks that the fast version agrees with the slow one."""
import random
import unittest

from snippets import way1_sets as w1
from snippets import way2_deque as w2
from snippets import way3_generators as w3
from snippets import way4_cache as w4
from snippets import way5_bisect as w5


class TestWay1Sets(unittest.TestCase):
    def test_same_count_for_list_and_set(self):
        rng = random.Random(1)
        for _ in range(50):
            items = [rng.randint(0, 100) for _ in range(rng.randint(0, 50))]
            queries = [rng.randint(-5, 105) for _ in range(30)]
            self.assertEqual(w1.count_hits(items, queries),
                             w1.count_hits(set(items), queries))

    def test_strings(self):
        animals = {"cat", "dog", "owl"}
        self.assertEqual(w1.count_hits(animals, ["dog", "cow", "owl"]), 2)


class TestWay2Deque(unittest.TestCase):
    def test_first_in_first_out(self):
        for n in (0, 1, 2, 10, 1000):
            self.assertEqual(w2.serve_with_list(n), list(range(n)))
            self.assertEqual(w2.serve_with_deque(n), list(range(n)))


class TestWay3Generators(unittest.TestCase):
    def test_same_sum(self):
        for n in (0, 1, 10, 12345):
            expected = (n - 1) * n * (2 * n - 1) // 6
            self.assertEqual(w3.sum_with_list(n), expected)
            self.assertEqual(w3.sum_with_generator(n), expected)

    def test_generator_memory_stays_small(self):
        n = 100_000
        self.assertLess(w3.peak_memory(w3.sum_with_generator, n), 10_000)
        self.assertGreater(w3.peak_memory(w3.sum_with_list, n), 1_000_000)


class TestWay4Cache(unittest.TestCase):
    def test_same_values(self):
        for n in range(25):
            self.assertEqual(w4.fib(n), w4.fib_cached(n))

    def test_each_value_computed_once(self):
        w4.fib_cached.cache_clear()
        w4.fib_cached(30)
        info = w4.fib_cached.cache_info()
        self.assertEqual((info.misses, info.hits), (31, 28))


class TestWay5Bisect(unittest.TestCase):
    def test_small_example(self):
        values = [1, 3, 3, 7]
        counts = [w5.count_below_sorted(values, t) for t in (0, 3, 4, 9)]
        self.assertEqual(counts, [0, 1, 3, 4])

    def test_same_counts(self):
        rng = random.Random(2)
        for _ in range(100):
            values = sorted(rng.randint(0, 20)
                            for _ in range(rng.randint(0, 40)))
            for t in range(-1, 23):
                self.assertEqual(w5.count_below(values, t),
                                 w5.count_below_sorted(values, t))
