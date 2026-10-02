FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y nodejs npm netcat

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 8080

CMD ["./wait-for", "database:27017", "--", "node", "server.js"]