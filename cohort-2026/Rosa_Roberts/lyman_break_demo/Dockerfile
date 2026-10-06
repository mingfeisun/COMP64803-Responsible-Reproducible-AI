FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir bagpipes matplotlib

# import once at build time so anything BAGPIPES downloads is baked into the image
RUN python -c "import bagpipes"

CMD ["bash"]