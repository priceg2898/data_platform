# Docker Housekeeping Guide

Docker images, containers, build cache, and volumes accumulate over time. Regular cleanup helps avoid wasted disk space and confusion from stale builds.

---

# Inspect Docker Disk Usage

## Summary

```bash
docker system df
```

## Detailed breakdown

```bash
docker system df -v
```

---

# Cleanup Commands

## Remove dangling images

Dangling images are untagged layers left behind after rebuilds.

```bash
docker image prune
```

Force without prompt:

```bash
docker image prune -f
```

---

## Remove unused images

Removes images not referenced by any container.

```bash
docker image prune -a
```

---

## Remove stopped containers

```bash
docker container prune
```

---

## Remove unused volumes

```bash
docker volume prune
```

---

## Remove unused networks

```bash
docker network prune
```

---

## Clean build cache

```bash
docker builder prune
```

More aggressive cleanup:

```bash
docker builder prune -a
```

---

# Full Cleanup

## Standard cleanup

```bash
docker system prune
```

## Aggressive cleanup

```bash
docker system prune -a --volumes
```

This removes:

- stopped containers
- unused networks
- unused images
- build cache
- unused volumes

⚠️ Be careful with `--volumes` if you store local databases or persistent data.

---

# Recommended Housekeeping Practices

## 1. Tag images intentionally

Avoid relying only on `latest`.

Prefer versioned tags:

```text
myapp:1.4.2
myapp:2026-05-12
myapp:git-sha
```

Benefits:

- easier rollback
- easier cleanup
- traceable deployments

---

## 2. Remove old tags after deployments

```bash
docker image rm myapp:old-tag
```

---

## 3. Use multi-stage builds

Reduces final image size dramatically.

Example:

```Dockerfile
FROM node:22 AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

---

## 4. Maintain a `.dockerignore`

Prevents unnecessary files from entering the build context.

Example:

```text
node_modules
.git
dist
coverage
.env
```

---

## 5. Inspect large images periodically

List images:

```bash
docker images
```

Inspect layers:

```bash
docker history myimage
```

---

## 6. Prefer slim runtime images

Examples:

```text
python:3.12-slim
node:22-alpine
```

Benefits:

- smaller downloads
- faster deployments
- reduced attack surface

---

## 7. Clean CI runners aggressively

Common CI cleanup:

```bash
docker system prune -af
docker builder prune -af
```

Useful for GitHub Actions runners, Jenkins agents, etc.

---

## 8. Use BuildKit cache management

If using `buildx`:

```bash
docker buildx prune
```

Aggressive cleanup:

```bash
docker buildx prune -a
```

---

# Useful Inspection Commands

## List all images

```bash
docker images -a
```

---

## Show image age

```bash
docker images --format "{{.Repository}}:{{.Tag}} {{.CreatedSince}}"
```

---

## Find containers using an image

```bash
docker ps -a --filter ancestor=myimage
```

---

# Suggested Maintenance Routine

## Weekly

```bash
docker image prune
docker builder prune
```

## Monthly

```bash
docker system prune
```

## Occasionally (deep cleanup)

```bash
docker system prune -a --volumes
```

Only run this when you understand what will be removed.

---

# Safety Notes

Be cautious about deleting:

- named volumes containing databases
- local development data
- images needed for offline work
- shared caches on build machines

Especially dangerous:

```bash
docker system prune -a --volumes
```

Review active containers and volumes before running aggressive cleanup commands.