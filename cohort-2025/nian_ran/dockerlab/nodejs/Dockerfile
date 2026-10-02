FROM ubuntu:xenial

# Install dependencies: nodejs, npm, and netcat (needed for wait-for)
RUN apt-get update && apt-get install -y curl netcat \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash - \
    && apt-get install -y nodejs

# Set the working directory
WORKDIR /app

# Copy everything into the container
COPY . /app

# Install Node.js dependencies
RUN npm install

# Expose port 8080 (because server listens here)
EXPOSE 8080

# Start command:
# Wait for MongoDB before starting Node.js
CMD ["./wait-for", "database:27017", "--", "npm", "start"]
