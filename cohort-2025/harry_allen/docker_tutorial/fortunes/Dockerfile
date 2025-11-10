FROM ubuntu:bionic

RUN apt-get update && \
	apt-get install -y fortune-mod fortunes-min && \
	rm -rf /var/lib/apt/lists/*

CMD ["/usr/games/fortune"] 
