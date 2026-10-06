#!/usr/bin/env bash
cd "$(dirname "$0")"
docker run --rm -v "$PWD":/app lsst-demo bash -c "python lyman_break_lsst.py"
open output/sed_vs_redshift.png