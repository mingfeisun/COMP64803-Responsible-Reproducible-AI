FROM ubuntu:22.04

# Install netcat, which is required by wait-for
RUN apt-get update && apt-get install -y nodejs npm netcat

# Set the working directory
WORKDIR /app

# Copy the application and install dependencies
COPY . .
RUN npm install

# Make wait-for executable
RUN chmod +x ./wait-for

# Application's port
EXPOSE 8080

# Wait for MongoDB, then start the application
CMD ["./wait-for", "database:27017", "--", "node", "server.js"]