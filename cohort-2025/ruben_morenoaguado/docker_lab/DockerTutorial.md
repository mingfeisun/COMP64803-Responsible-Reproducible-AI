# Docker Tutorial

## Notes

After installing the desktop app on mac, add this line to `~/.zprofile`:

```
export PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin/"
```

## Questions

1. What user are you logged in as by default?

root

2. If you start and then exit an interactive container, and then use the docker run -it ubuntu:xenial /bin/bash command again, is it the same container? How can you tell?

It is a different container. I can tell by seeing in the Docker app that a new docker container with a different id has been created. Also by running `docker ps -a`, which shows all containers even ones that are no longer running. 

3. Run the image you just built. Since we specified the default CMD, you can just do docker run -it mypython:latest. What do you observe?

I see the python interactive interpreter. 

4. Write and build a Dockerfile that installs the packages fortune and fortunes-min and runs the fortune executable (located in /usr/games/fortune after you install it). Note that you won’t need to use the -it flags when you run the container as fortune doesn’t need STDIN. Submit your Dockerfile with this lab. Hint: if you’re having trouble writing your Dockerfile, try booting an interactive container and installing both packages. Translate what you did into a Dockerfile. How can you translate what you did interactively to a Dockerfile?

Creating a docker image from another image:

`docker run ubuntu:bionic` $\rightarrow$ `FROM ubuntu:bionic`

Installing software (or general setup code):

`apt-get install -y <package-name(s)>` $\rightarrow$ `RUN apt-get install -y fortune fortunes-min`

Running a command on startup:

`/usr/games/fortune` $\rightarrow$ `CMD ['/usr/games/fortune']`

5. Paste the output of your docker images command after questions 1 and 2.

```
$ docker run -it mypython:latest
Python 3.6.9 (default, Mar 10 2023, 16:46:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

$ docker run fortunes
Your lucky number is 3552664958674928.  Watch for it everywhere.
```

6. With httpd running in a detached container, run /bin/bash on the same container and paste the output of ps aux. Observe that there’s very few processes running as compared to running ps aux on your VM. Why is this the case?

The container is built on a minimal system and only runs processes that are necessary for the software it encapsulates.

