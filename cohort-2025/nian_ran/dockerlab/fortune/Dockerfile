FROM ubuntu:bionic

COPY . .

RUN apt-get update && apt-get install -y fortune fortunes-min --no-install-recommends
CMD ["/usr/games/fortune"]