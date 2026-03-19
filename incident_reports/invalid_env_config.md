# Incident: Invalid Database Credentials

## 1. Symptoms

* API endpoint `/api/db-check` returned:

  ```json
  {"db": "failed"}
  ```
* Nginx and API were reachable
* Error observed in API logs:

  ```
  password authentication failed for user "admin"
  ```

## 2. Root Cause

* Incorrect `DB_PASSWORD` was configured in `.env`
* API attempted to connect using invalid credentials
* PostgreSQL rejected the connection

## 3. Debugging Steps

1. Verified API response:

   ```bash
   curl http://localhost:8080/api/db-check
   ```

2. Checked API logs:

   ```bash
   docker compose logs api
   ```

3. Observed authentication failure message

4. Verified `.env` configuration mismatch

## 4. Fix Applied

* Corrected `.env`:

  ```env
  DB_PASSWORD=secret
  ```

* Restarted services:

  ```bash
  docker compose down
  docker compose up -d --build
  ```

* Verified recovery:

  ```bash
  curl http://localhost:8080/api/db-check
  ```
  
## 5. Key Learnings

* Not all connection failures are network-related
* Authentication errors must be distinguished from connectivity issues
* Logs are essential to differentiate failure types
* Configuration management is critical in distributed systems
