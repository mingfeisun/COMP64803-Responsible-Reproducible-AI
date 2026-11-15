# Five ways to write better Python (COMP64803 talk).
# Everything runs on the Python standard library, so there is nothing to pip install.
#
#   docker build -t five-ways .                                  build the image
#   docker run --rm five-ways                                    run the five demos
#   docker run --rm five-ways python -m unittest -v              run the 9 tests
#   docker run --rm five-ways python snippets/way1_sets.py       run one way
#   docker run --rm -it five-ways bash                           open a shell inside

# This tag gives everyone the same interpreter, Python 3.13 on Debian slim.
FROM python:3.13-slim

# Print output straight away (useful for a live demo) and keep .pyc files out of the image.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY run_all.py ./
COPY snippets/ snippets/
COPY tests/ tests/

CMD ["python", "run_all.py"]
