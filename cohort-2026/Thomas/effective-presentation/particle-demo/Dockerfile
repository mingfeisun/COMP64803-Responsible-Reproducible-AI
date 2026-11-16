FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulation.py .
COPY tests.py .

CMD ["sh", "-c", "python simulation.py && python -m unittest tests -v"]