
# Docker Compose Exercise

## COMP64803 - Introduction to Responsible & Reproducible AI

This exercise demonstrates how Docker Compose can be used to run a Node.js web application and a MongoDB database in separate, connected containers.

## Application

Original application:
https://github.com/0xcf/decal-sp18-a10

The application source code is included for reproducibility. The original project is distributed under the MIT licence, which is retained in this directory.

## Docker Configuration

- Node.js 16 (legacy compatibility)
- MongoDB 4.4 (legacy compatibility)
- Docker Compose
- Application port: 8080

These older versions are used for the course exercise and are not recommended for production deployment.

## Running the Application

From this directory, run:

```bash
docker compose up --build -d
```

To check that the application is responding:

```bash
curl http://localhost:8080
```

To stop and remove the containers:

```bash
docker compose down
```

## Results

Both the Node.js and MongoDB containers started successfully.

The application returned HTTP status 200, confirming that the web server responded successfully.
