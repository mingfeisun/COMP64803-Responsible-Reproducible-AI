FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir torch==2.1.0 numpy==1.26.4

RUN chmod +x tip3_117.sh

# Default command
CMD ["python", "tip1_92.py"]
