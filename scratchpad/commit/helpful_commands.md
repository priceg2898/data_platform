| Command | Description |
| -------- | -----------|
| `docker compose -f docker/long_running/minio/docker-compose.yaml down -v` | Docker compose while passing a filepath |
| `docker build -f ./docker/ephemeral/Dockerfile__ephemeral_etl -t ephemeral_etl .` | Build a docker image based on a Dockerfile, container name, and build context |
| `du -h / \| sort -h \| tail -30` | Bash command to display size of files, sort highest to lowest, and return the last 30 rows |