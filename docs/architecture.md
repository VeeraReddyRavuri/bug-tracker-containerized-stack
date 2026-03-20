# Architecture Overview

## System Components

### Client

Represents the end user making HTTP requests via browser or curl.

### Nginx (Reverse Proxy)

Acts as the single entry point to the system.

* Listens on port 8080
* Routes incoming requests to backend API containers
* Performs load balancing across multiple API instances

### FastAPI (Backend API)

Handles application logic and exposes endpoints:

* `/health` → service health
* `/api/db-check` → database connectivity
* `/api/whoami` → load balancing verification

Runs as multiple containers for scalability.

### PostgreSQL (Database)

Stores application data.

* Runs as a separate container
* Uses a Docker volume for persistent storage

### Docker Network

A custom bridge network that enables communication between services using service names:

* `api` → backend containers
* `db` → database container

### Docker Volume

Ensures PostgreSQL data persists across container restarts.

## Request Flow

1. Client sends request to:

   ```
   http://localhost:8080
   ```

2. Request reaches Nginx (reverse proxy)

3. Nginx forwards request to one of the API containers

4. API processes request:

   * If DB interaction is needed → connects to PostgreSQL using:

     ```
     db:5432
     ```

5. Response flows back:

   ```
   PostgreSQL → API → Nginx → Client
   ```

## Scaling Behavior

* API service can be scaled using:

  ```bash
  docker compose up --scale api=2
  ```

* Nginx load balances requests across API containers

* Docker DNS resolves `api` to multiple container IPs

## Failure Handling

### Database Down

* API does not crash
* Returns controlled failure response
* Logs error for debugging

### Invalid Configuration

* Authentication errors are logged
* System continues running

### Nginx Load Balancing Issue

* Resolved using:

  * Docker DNS resolver
  * Shared memory (`zone`)
  * Dynamic upstream resolution

## Key Design Decisions

### Containerized Architecture

Each service runs in an isolated container to ensure modularity and portability.

### Environment-Based Configuration

All configuration is externalized using `.env` to avoid hardcoding.

### Service-to-Service Communication

Containers communicate using service names via Docker DNS instead of static IPs.

### Reverse Proxy Layer

Nginx provides a single entry point and abstracts backend scaling.

## Data Persistence

* PostgreSQL data is stored in a Docker volume:

  ```
  /var/lib/postgresql/data
  ```

* Ensures data is not lost on container restart

## Summary

This architecture demonstrates:

* Multi-service communication
* Reverse proxy routing
* Horizontal scaling
* Failure handling in distributed systems
