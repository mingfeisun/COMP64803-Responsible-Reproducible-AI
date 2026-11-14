# Docker Tutorial — Dockerfiles

**Module:** COMP64803 – Responsible and Reproducible AI

## Question 1: Running a Python Docker Image

**Question:** Run the image you just built using `docker run -it mypython:latest`. What do you observe?

**Command:**

```bash
docker run -it mypython:latest
```

**Answer:**

When the container starts, it automatically launches an interactive Python interpreter rather than a Bash shell. This happens because the `CMD` instruction in the Dockerfile specifies Python as the default executable.

The `-it` flags allow us to interact with the Python interpreter by typing Python commands directly into the terminal.

The container uses the Python environment installed during the image-building process.

## Question 2: Creating a Fortune Docker Image

**Question:** Write and build a Dockerfile that installs Fortune and `fortunes-min` and runs the Fortune executable.

**Dockerfile:**

```dockerfile
FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y fortune-mod fortunes-min && \
    rm -rf /var/lib/apt/lists/*

CMD ["/usr/games/fortune"]
```

**Building the image:**

```bash
docker build -t myfortune:latest .
```

**Running the container:**

```bash
docker run myfortune:latest
```

**Output from first execution:**

```text
An honest tale speeds best being plainly told.
        -- William Shakespeare, "Henry VI"
```

**Output from second execution:**

```text
Your goose is cooked.
(Your current chick is burned up too!)
```

**Answer:**

The Dockerfile uses Ubuntu 24.04 as the base image and installs `fortune-mod` and `fortunes-min` using `apt-get`.

The `RUN` instruction executes during the image-building process to install the necessary packages, while the `CMD` instruction specifies the Fortune executable to run when a container starts.

When the container is executed, it prints a randomly selected fortune and then terminates.

Unlike the Python example, the `-it` flags are unnecessary because Fortune does not require interactive input.

The commands that would normally be executed manually inside an interactive container are translated into `RUN` instructions in the Dockerfile. This automates the environment setup and makes it reproducible.

## Question 3: Docker Images

**Question:** Paste the output of the `docker images` command after completing Questions 1 and 2.

**Command:**

```bash
docker images
```

**Terminal output:**

```text
IMAGE                ID             DISK USAGE
fedora:latest        43b29f65a41e        276MB
hello-world:latest   c567b231f656       25.9kB
myfortune:latest     b78cc9dc0e94        121MB
mypython:latest      d25d218a3ad4        219MB
ubuntu:24.04         2198e4c65076        119MB
ubuntu:bionic        152dc042452c       97.5MB
ubuntu:latest        6a06111c3b0a        163MB
ubuntu:xenial        1f1a2d56de1d        195MB
```

**Observation:**

The output confirms that both custom Docker images, `mypython:latest` and `myfortune:latest`, were successfully built and stored locally.

The images have different image IDs and disk usage because they contain different software packages and dependencies.



###################################

## Detached Containers and Ports

### Question: Why are fewer processes running inside the Docker container compared to the host machine?

**1. Running Apache in detached mode**

```bash
docker run -d -p 5050:80 --name apache-server httpd
```

The `-d` flag runs the container in the background, while `-p 5050:80` forwards port 5050 on the host to port 80 inside the container.

I verified that the Apache server was running using:

```bash
curl http://localhost:5050
```

The response contained:

```html
<title>It works! Apache httpd</title>
<p>It works!</p>
```

This confirmed that the Apache web server was accessible through the forwarded port.

**2. Inspecting processes inside the container**

I accessed the running container using:

```bash
docker exec -it apache-server /bin/bash
```

Initially, `ps aux` returned `bash: ps: command not found`, so I installed the required package:

```bash
apt-get update
apt-get install -y procps
```

I then executed:

```bash
ps aux
```

**Output:**

```text
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   6224  4944 ?        Ss   17:14   0:00 httpd -DFOREGROUND
www-data       8  0.0  0.0 1997408 4292 ?        Sl   17:14   0:00 httpd -DFOREGROUND
www-data       9  0.0  0.0 1997408 4296 ?        Sl   17:14   0:00 httpd -DFOREGROUND
www-data      10  0.0  0.0 1997464 4816 ?        Sl   17:14   0:00 httpd -DFOREGROUND
root          92  0.1  0.0   4328  3732 pts/0    Ss   17:16   0:00 /bin/bash
root         221  0.0  0.0   6400  3768 pts/0    R+   17:17   0:00 ps aux
```

**3. Comparing with the host machine**

After exiting the container, I ran `ps aux` on the host machine.

The host displayed considerably more processes, including system services, kernel threads, desktop applications, and background processes.

**4. Explanation**

The Docker container displays significantly fewer processes because Docker uses Linux namespaces to provide process isolation.

In particular, **PID namespaces** isolate the process identifiers visible inside a container. Consequently, processes running on the host or in other containers are generally not visible from inside the Apache container.

The container primarily runs the processes required for its intended application:

- `httpd -DFOREGROUND` (PID 1): The main Apache server process.
- `httpd -DFOREGROUND` (PIDs 8–10): Apache worker processes running as `www-data`.
- `/bin/bash` (PID 92): The interactive shell started using `docker exec`.
- `ps aux` (PID 221): The command used to inspect the running processes.

In contrast, the host operating system manages the entire computing environment, including hardware-related processes, background services, user applications, and Docker itself.

**Conclusion:** Docker containers provide process isolation through Linux namespaces. This allows applications to run in relatively lightweight, isolated environments without requiring a separate operating-system kernel for each container.
