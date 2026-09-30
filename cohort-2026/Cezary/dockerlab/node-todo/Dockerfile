FROM ubuntu:xenial

RUN apt-get update && apt-get install -y nodejs npm netcat

WORKDIR /app

COPY . .

RUN npm install

RUN chmod +x wait-for

EXPOSE 8080

CMD ["./wait-for", "database:27017", "--", "nodejs", "server.js"]

