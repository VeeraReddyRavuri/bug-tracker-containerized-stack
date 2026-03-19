# Incident: Database Connection Failure

## 1. Symptoms

* API endpoint `/api/db-check` returned:

  ```json
  {"db": "failed"}
  ```
* Nginx was reachable, API was running
* Error observed in API logs:

  ```
  DB connection failed: could not translate host name "db" to address
  ```

## 2. Root Cause

* PostgreSQL container was stopped
* Docker DNS could not resolve the hostname `db`
* API depends on Docker service name for DB connection

## 3. Debugging Steps

1. Verified API response:

   ```bash
   curl http://localhost:8080/api/db-check
   ```

2. Checked API logs:

   ```bash
   docker compose logs api
   ```

3. Observed DNS resolution failure for `db`

4. Verified DB container status:

   ```bash
   docker compose ps
   ```

## 4. Fix Applied

* Restarted DB container:

  ```bash
  docker compose up -d db
  ```

* Verified recovery:

  ```bash
  curl http://localhost:8080/api/db-check
  ```
  
## 5. Key Learnings

* Docker service names rely on internal DNS
* If a container stops, its DNS entry is removed
* Applications must handle DB failures gracefully
* Logging is critical for identifying root cause
