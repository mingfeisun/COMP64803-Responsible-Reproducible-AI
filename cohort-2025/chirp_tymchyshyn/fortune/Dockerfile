FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y fortune fortunes-min && \
    rm -rf /var/lib/apt/lists/*

CMD ["/usr/games/fortune"]