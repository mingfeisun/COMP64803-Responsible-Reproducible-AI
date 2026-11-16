# Wiener-Hopf Monte Carlo pricing of barrier options (Black-Scholes).
# Pinned interpreter and libraries so every run gives the same numbers
# (Effective Python, Item 1: know which version of Python you're using).
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import matplotlib.pyplot"   # build the font cache once, at build time

COPY whmc/ ./whmc/
COPY run_pricing.py pyproject.toml ./
COPY tests/ ./tests/

# Default: price the option and print the convergence study.
# Tests:   docker run --rm whmc-barrier python -m pytest -q tests
# Figures: docker run --rm -v "$PWD/figures:/app/results" whmc-barrier
CMD ["python", "run_pricing.py"]
