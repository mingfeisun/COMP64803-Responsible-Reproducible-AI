# Dockerfile for Effective Python Demos
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all demo files
COPY *.py .
COPY *.md .

# Make run_all_demos.py executable
RUN chmod +x run_all_demos.py

# Set default command to run all demos
CMD ["python", "run_all_demos.py"]

# Alternative: Run interactive Python
# CMD ["python"]

# To run a specific demo:
# docker run effective-python python 1_comprehensions_generators.py