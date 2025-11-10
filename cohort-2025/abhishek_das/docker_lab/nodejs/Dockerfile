FROM ubuntu:xenial 

RUN apt-get update && \
    # download and run NodeSource setup script for Node.js 14
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    # create a symlink as app expects node, but called nodejs on ubuntu
    ln -s /usr/bin/nodejs /usr/bin/node && \
    # install app and libs
    apt-get install -y npm nodejs netcat git && \ 
    git clone https://github.com/0xcf/decal-sp18-a10.git /usr/src/app

WORKDIR /usr/src/app
RUN npm install
RUN chmod +x wait-for


EXPOSE 8080

CMD ["./wait-for", "database:27017", "--", "node", "server.js"]
