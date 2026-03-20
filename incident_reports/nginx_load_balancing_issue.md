# Incident: Nginx Not Load Balancing Across Multiple API Containers

## 1. Symptoms

* API was scaled to multiple containers using:

  ```bash
  docker compose up -d --scale api=2
  ```
* Requests to `/api/whoami` always returned the same container ID
* Load was not distributed across API instances

## 2. Root Cause

* Nginx resolves upstream service names only once at startup
* It cached a single IP address for the `api` service
* As a result, all traffic was routed to only one container
* Dynamic resolution was not configured

## 3. Debugging Steps

1. Verified multiple API containers were running:

   ```bash
   docker compose ps
   ```

2. Tested endpoint multiple times:

   ```bash
   curl http://localhost:8080/api/whoami
   ```

3. Observed same container responding every time

4. Checked Nginx logs:

   ```bash
   docker compose logs nginx
   ```

5. Identified error related to dynamic DNS resolution and missing shared memory

## 4. Fix Applied

* Enabled Docker DNS resolver in Nginx:

  ```nginx
  resolver 127.0.0.11 valid=5s;
  ```

* Updated upstream block to support dynamic resolution:

  ```nginx
  upstream api {
      zone api 64k;
      least_conn;
      server api:8000 resolve;
  }
  ```

* Restarted services:

  ```bash
  docker compose down
  docker compose up -d
  ```

* Verified load balancing:

  ```bash
  curl http://localhost:8080/api/whoami
  ```

## 5. Key Learnings

* Nginx caches DNS by default and does not automatically detect new containers
* Dynamic service discovery requires explicit configuration
* Shared memory (`zone`) is required for runtime DNS resolution in Nginx
* Scaling services without proper load balancing configuration is ineffective
