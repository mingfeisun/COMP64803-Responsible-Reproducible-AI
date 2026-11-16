#!/usr/bin/env bash
# Runs the five demos in talk order.
set -e
python --version
for demo in item52_subprocess item30_generators item64_parallel item70_profile item76_tests; do
    echo
    echo "========== $demo =========="
    python "$demo.py"
done
