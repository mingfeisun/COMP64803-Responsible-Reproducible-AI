docker build -t particle-demo .
docker run --rm -v "$(pwd):/app" particle-demo