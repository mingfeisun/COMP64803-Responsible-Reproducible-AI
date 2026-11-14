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
