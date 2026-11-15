
FROM node:16-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY package*.json ./

RUN npm install

COPY . .

RUN chmod +x wait-for

EXPOSE 8080

CMD ["./wait-for", "database:27017", "-t", "60", "--", "node", "server.js"]
