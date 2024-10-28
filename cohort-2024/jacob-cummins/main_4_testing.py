import unittest

from main_4_code import fibonacci, fibonacci_number_matcher

class TestFibonacciFunctions(unittest.TestCase):
    
    def test_fibonacci_sequence(self):
        # Test cases for fibonacci sequence generation
        test_cases = [
            (0, []),               # n=0 should return an empty list
            (1, [0]),              # n=1 should return [0]
            (2, [0, 1]),           # n=2 should return [0, 1]
            (5, [0, 1, 1, 2, 3]),  # n=5 should return first 5 Fibonacci numbers
            (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]) # First 10 Fibonacci numbers
        ]
        
        for n, expected_sequence in test_cases:
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), expected_sequence)
    
    def test_fibonacci_number_matcher(self):
        # Test cases for matching numbers containing specific substrings
        test_cases = [
            (10, 1, [1, 1, 13, 21]),     # Check for Fibonacci numbers containing '1'
            (30, 999, []),           # Check for a substring that doesn't appear
            (0, 3, []),              # Edge case: n=0 should return an empty list regardless of 'contains'
            (1, 0, [0]),              # Edge case: n=1 should only return [0]
            (-1, 1, [])              # Edge case: n=-1 should return an empty list regardless of 'contains'
        ]
        
        for n, contains, expected_matches in test_cases:
            with self.subTest(n=n, contains=contains):
                self.assertEqual(fibonacci_number_matcher(n, contains), expected_matches)


if __name__ == "__main__":
    unittest.main()