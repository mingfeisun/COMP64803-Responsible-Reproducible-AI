
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


class TestEffectivePythonExamples(unittest.TestCase):

    def run_demo(self, filename):
        result = subprocess.run(
            [sys.executable, str(PROJECT_DIR / filename)],
            capture_output=True,
            text=True,
            timeout=120
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout + result.stderr
        )

        return result.stdout

    def test_01_lie_brackets(self):
        output = self.run_demo("01_lie_brackets.py")

        self.assertIn(
            "All Lie algebra checks passed!",
            output
        )

    def test_02_s3_characters(self):
        output = self.run_demo("02_s3_characters.py")

        self.assertIn(
            "Transposition: Before = 0, After = 0",
            output
        )
        self.assertIn(
            "All S3 character checks passed!",
            output
        )

    def test_03_symmetric_groups(self):
        output = self.run_demo("03_symmetric_groups.py")

        self.assertIn(
            "All S4 conjugacy class checks passed!",
            output
        )

    def test_04_young_tableaux(self):
        output = self.run_demo("04_young_tableaux.py")

        self.assertIn(
            "Total possible tableaux: 16796",
            output
        )
        self.assertIn(
            "Item 81: Memory profiling",
            output
        )
        self.assertIn(
            "All Young tableaux checks passed!",
            output
        )

    def test_05_profiling(self):
        output = self.run_demo("05_profiling.py")

        self.assertIn(
            "Before (enumeration): 48620",
            output
        )
        self.assertIn(
            "After (binomial formula): 48620",
            output
        )
        self.assertIn(
            "All profiling checks passed!",
            output
        )


if __name__ == "__main__":
    unittest.main()
