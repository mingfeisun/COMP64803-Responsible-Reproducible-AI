FROM python:3.12.7-slim

WORKDIR /app

# Install dependencies first (cached unless requirements.txt changes)
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the script and the input file
COPY python_70.py .
COPY hydrogen.xyz .

CMD ["python", "python_70.py"]
