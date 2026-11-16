"""Item 52: Use subprocess to manage child processes.

Starts several simulations at once, each as its own child process, and
waits for them with a time limit. One run has bad input and one would run
far too long, to show the script copes with both.

Run: python item52_subprocess.py
"""
import subprocess
import sys
import time
from pathlib import Path

# The folder this script is in, so it works whichever folder you run it from
HERE = Path(__file__).parent

TIME_LIMIT = 5  # seconds

# name of run -> (temperature, number of steps)
runs = {
    "T0.5": ("0.5", "200"),
    "T1.0": ("1.0", "200"),
    "T1.5": ("1.5", "200"),
    "bad_input": ("-1", "200"),     # negative temperature: will fail
    "too_slow": ("1.0", "100000"),  # would take ~17 minutes: will be stopped
}

# 1. Start every run. Popen returns straight away and the run carries on
#    in the background, so all five run at the same time.
processes = {}
for name, (temp, steps) in runs.items():
    # The command is a list, not one long string: no quoting problems.
    cmd = [sys.executable, "fake_md.py", temp, steps, f"sim_{name}.txt"]
    processes[name] = subprocess.Popen(
        cmd, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
start = time.time()

# 2. Collect the results, never waiting past the time limit.
for name, proc in processes.items():
    time_left = max(0, TIME_LIMIT - (time.time() - start))
    try:
        output, _ = proc.communicate(timeout=time_left)
        if proc.returncode == 0:
            print(f"{name:<10} ok        {output.strip()}")
        else:
            print(f"{name:<10} FAILED    exit code {proc.returncode}: {output.strip()}")
    except subprocess.TimeoutExpired:
        proc.kill()         # stop it, so it doesn't keep using a CPU core
        proc.communicate()  # tidy up the stopped process
        print(f"{name:<10} STOPPED   still running after {TIME_LIMIT} s")