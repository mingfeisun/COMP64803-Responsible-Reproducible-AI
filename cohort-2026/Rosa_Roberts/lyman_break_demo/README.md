# Lyman-break windows in the LSST filters

At what redshifts does the Lyman-α break move through each of the six LSST
filters (*ugrizy*)?

`lyman_break_lsst.py` loads the LSST total-throughput curves, builds a
BAGPIPES model galaxy at several redshifts (BAGPIPES applies the IGM
absorption that creates the break), and:

- plots the model SED over the filter curves at each redshift
  → `output/sed_vs_redshift.png`
- works out the redshift range over which the break falls inside each band
  and plots it as horizontal bars → `output/lyman_break_windows.png`

## Project layout

```
lyman_break_demo/
├── Dockerfile
├── build.sh               # builds the Docker image
├── run.sh                 # runs the script in the container and opens the plot
├── lyman_break_lsst.py
├── throughputs/
│   └── baseline/
│       └── total_{u,g,r,i,z,y}.dat   # LSST total-throughput curves
└── output/                # created when the script runs
```

The throughput files come from the LSST throughputs repository
(<https://github.com/lsst/throughputs>, `baseline/` folder). Their first
column is wavelength in nm and the second is total throughput.

## Running with Docker

The image contains Python 3.11, BAGPIPES and matplotlib. Your project folder
is **mounted** into the container at `/app`, so you can edit the script
without rebuilding.

**1. Build the image** (only needed once, or after changing the Dockerfile):

```bash
./build.sh
# or, equivalently:
docker build -t lsst-demo .
```

**2. Run the script:**

```bash
./run.sh
# or, equivalently:
docker run --rm -v "$PWD":/app lsst-demo python lyman_break_lsst.py
```

`run.sh` also opens the SED figure afterwards. It uses `open`, which is a
macOS command; on Linux, use `xdg-open` instead.
