FROM node:12-buster

WORKDIR /app

# Use archived Debian repositories because Buster is end-of-life
RUN printf 'deb http://archive.debian.org/debian buster main\n' > /etc/apt/sources.list && \
    printf 'deb http://archive.debian.org/debian-security buster/updates main\n' >> /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY package*.json ./

RUN npm install

COPY . .

RUN chmod +x wait-for

EXPOSE 8080

CMD ["./wait-for", "database:27017", "-t", "60", "--", "node", "server.js"]
