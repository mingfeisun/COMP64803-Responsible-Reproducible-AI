FROM python:3.11-slim

# Install bash 
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Copy scripts into container
COPY scripts/ /app/scripts/

# Set working directory to scripts dir
WORKDIR /app/scripts

# Default command: open interactive bash shell
CMD ["/bin/bash"]
