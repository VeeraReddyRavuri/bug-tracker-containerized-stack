# Incident: Port Conflict on Host (8080)

## 1. Symptoms

* Attempted to start application stack
* No visible error during container startup
* Requests to `localhost:8080` returned unexpected responses (Python HTTP server instead of Nginx)

## 2. Root Cause

* Port 8080 was already occupied by a Python HTTP server:

  ```bash
  python3 -m http.server 8080
  ```
* Due to Docker Desktop (WSL) networking behavior, conflict was not explicitly thrown
* Traffic was routed to the host process instead of Docker container

## 3. Debugging Steps

1. Verified response headers:

   ```bash
   curl -I http://localhost:8080
   ```

   Observed:

   ```
   Server: SimpleHTTP/0.6 Python/3.12.3
   ```

2. Checked port usage:

   ```bash
   lsof -i :8080
   ```

   Found Python process listening

3. Compared with Docker containers:

   ```bash
   docker ps
   ```

   Observed nginx container mapped to port 8080

## 4. Fix Applied

* Stopped Python server occupying port 8080:

  ```bash
  CTRL + C
  ```

* Restarted Docker stack:

  ```bash
  docker compose down
  docker compose up -d
  ```

* Verified correct routing:

  ```bash
  curl http://localhost:8080/health
  ```

## 5. Key Learnings

* Port conflicts may behave differently in WSL vs native Linux
* Always verify actual service responding via headers
* Use `lsof` or `ss` to identify port ownership
* Do not assume Docker errors will always surface explicitly
* Host-level debugging is critical in distributed systems