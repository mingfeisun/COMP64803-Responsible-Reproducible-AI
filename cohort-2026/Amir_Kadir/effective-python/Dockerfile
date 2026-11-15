

FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir sympy==1.13.3

COPY *.py .

CMD ["python", "01_lie_brackets.py"]
