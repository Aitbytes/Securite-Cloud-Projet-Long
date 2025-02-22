# List files
docker-compose run --rm drive-watcher list

# Download and process a file
docker-compose run --rm drive-watcher get --file-id YOUR_FILE_ID

# Watch a file
docker-compose run --rm drive-watcher watch --file-id YOUR_FILE_ID --interval 5
