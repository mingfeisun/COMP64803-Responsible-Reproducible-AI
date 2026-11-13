FROM python:3.13.6-slim

WORKDIR /app

# Copy the script into the container workspace (Run python_{integer}.py . for another item)
COPY python_75.py .

# Run the script when the container starts
CMD ["python", "python_75.py"]
