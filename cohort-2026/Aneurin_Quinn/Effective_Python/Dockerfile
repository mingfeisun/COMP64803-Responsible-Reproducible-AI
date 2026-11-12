# Reproducible environment for the Effective Python demos.
# Pinned interpreter version: see Item 1 ("Know which version of Python you're using").
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY snippets/ ./snippets/
COPY tests/ ./tests/

# Default: run all five live demos. Override to run tests or a single item.
CMD ["python", "snippets/run_all.py"]
