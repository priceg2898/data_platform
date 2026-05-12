docker compose -f docker/long_running/minio/docker-compose.yaml down -v
docker build -f ./docker/ephemeral/Dockerfile__ephemeral_etl -t ephemeral_etl . 
du -h / | sort -h | tail -30