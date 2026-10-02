FROM python:3.12-slim

WORKDIR /app
COPY . /app

# Install uv
RUN apt-get update && apt-get install -y curl && \
 curl -LsSf https://astral.sh/uv/install.sh | sh && \
 rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
RUN uv sync --frozen

# Prepare dataset
RUN uv run python prepare_data.py

ENTRYPOINT ["uv", "run", "python", "main.py"]