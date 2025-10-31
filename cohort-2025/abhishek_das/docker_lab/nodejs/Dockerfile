FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    curl \
    netcat \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN npm install

EXPOSE 8080

CMD ["./wait-for", "database:27017", "--", "npm", "start"]
