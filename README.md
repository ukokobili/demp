Method 1: Using Docker CLI Commands:

Stop all running containers:
```Bash
docker stop $(docker ps -a -q)
```

Remove all stopped containers:
```Bash
docker rm $(docker ps -a -q)
```

Remove all volumes:

For anonymous volumes:
```Bash
docker volume prune
```
For named volumes (optional):
```Bash
docker volume ls | awk '{print $2}' | xargs docker volume rm
```

Method 2: Using Docker Compose:

Down all services:
```Bash
docker-compose down
```

Optionally remove volumes:
```Bash
docker-compose down -v
```