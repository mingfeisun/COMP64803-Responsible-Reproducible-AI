FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN chmod +x wait-for
EXPOSE 8080
CMD ["./wait-for", "database:27017", "--", "nodejs", "server.js"]
