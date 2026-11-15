
FROM node:14.21.3-bullseye-slim

# set the working directory
WORKDIR /app

# install netcat for wait-for
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# install Node.js 
COPY package.json ./
RUN npm install --production --no-audit --no-fund

# copy this application source code
COPY . .

# set wait-for running for the application
RUN chmod +x ./wait-for

# document the application port
EXPOSE 8080

# before starting Node.js, wait for MongoDB
CMD ["./wait-for", "database:27017", "-t", "60", "--", "node", "server.js"]

