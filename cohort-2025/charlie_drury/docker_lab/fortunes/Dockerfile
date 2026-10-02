# use lightweight ubuntu image
FROM ubuntu:bionic

# install fortunes packages
RUN apt-get update && \
    apt-get install -y fortune-mod fortunes-min 
    
# run command
CMD ["/usr/games/fortune"]