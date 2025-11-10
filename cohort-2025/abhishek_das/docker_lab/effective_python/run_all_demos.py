#!/usr/bin/env python3
"""
Master script to run all Python effectiveness demos
"""

import subprocess
import sys
from pathlib import Path


def run_demo(script_name: str, title: str):
    """Run a single demo script"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        return False
    
    return True


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "    🐍 EFFECTIVE PYTHON: 5 ESSENTIAL TECHNIQUES    ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demos = [
        ("1_comprehensions_generators.py", "1️⃣  List Comprehensions & Generators"),
        ("2_context_managers.py", "2️⃣  Context Managers (with statements)"),
        ("3_type_hints_validation.py", "3️⃣  Type Hints & Data Validation"),
        ("4_itertools_demo.py", "4️⃣  Efficient Data Processing (itertools)"),
        ("5_fstrings_logging.py", "5️⃣  F-strings & Logging"),
    ]
    
    results = []
    
    for script, title in demos:
        if Path(script).exists():
            success = run_demo(script, title)
            results.append((title, success))
        else:
            print(f"❌ Script not found: {script}")
            results.append((title, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("  DEMO SUMMARY")
    print("=" * 70)
    
    for title, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {title}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print("\n" + "=" * 70)
    print(f"  Completed: {successful}/{total} demos")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()