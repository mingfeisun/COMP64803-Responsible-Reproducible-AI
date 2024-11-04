#!/bin/bash

IMAGE_NAME="python-scripts-demo"

echo "Building the Docker image..."
docker build -t $IMAGE_NAME .

echo "Running the Docker container with interactive shell..."
docker run -it --rm $IMAGE_NAME
