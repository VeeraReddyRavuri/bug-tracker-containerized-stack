# Incident: Connection Refused vs Timeout vs DNS Failure

## 1. Symptoms

* API failed to connect to database
* Observed different types of errors:

  * DNS resolution failure
  * Authentication failure

## 2. Root Cause

Different failure modes correspond to different layers:

* DNS failure:

  * Occurs when DB container is stopped or removed
  * Docker DNS no longer resolves service name `db`

* Connection refused (conceptual):

  * Host reachable, but service not listening on port

* Timeout:

  * Network issue, host unreachable

## 3. Debugging Steps

1. Tested connectivity:

   ```bash
   nc -zv db 5432
   ```

2. Observed DNS failures:

   ```
   Temporary failure in name resolution
   ```

3. Verified container state:

   ```bash
   docker compose ps
   ```

4. Tested service availability via API endpoint:

   ```bash
   curl http://localhost:8080/api/db-check
   ```

---

## 4. Fix Applied

* Restarted DB container:

  ```bash
  docker compose up -d db
  ```

* Verified connectivity restored:

  ```bash
  nc -zv db 5432
  ```

---

## 5. Key Learnings

* Networking issues must be diagnosed layer-by-layer:

  * DNS → TCP → Application
* Docker behavior differs from traditional systems:

  * Stopping a container removes its DNS entry
* Not all failures produce "connection refused"
* Understanding failure types is critical for debugging distributed systems
