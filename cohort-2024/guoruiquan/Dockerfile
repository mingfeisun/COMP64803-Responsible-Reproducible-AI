FROM pytorch/pytorch:latest
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
CMD ["python", "main.py"]