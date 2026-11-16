# 1. Start from an official image that already has Python 3.13 installed.
#    (Effective Python, Item 1: know which version of Python you're using.)
FROM python:3.13-slim

# 2. All later commands run inside /app in the container.
WORKDIR /app

# 3. Install the pinned dependencies first. Docker caches this layer, so
#    editing the code does not trigger a re-install.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the code into the image.
COPY . .

# 5. What `docker run` does when you give it no other command.
CMD ["python", "-m", "zprime.demo", "all"]
