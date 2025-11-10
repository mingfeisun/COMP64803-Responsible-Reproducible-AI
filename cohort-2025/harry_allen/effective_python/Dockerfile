FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
 && rm -rf /var/lib/apt/lists/*

COPY scripts/ /app/scripts/

WORKDIR /app/scripts

CMD ["/bin/bash"]
