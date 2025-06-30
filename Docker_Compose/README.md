# Docker Compose Flask Application

This project demonstrates a simple Flask web application with Redis as a counter backend, orchestrated using Docker Compose.

## What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services, networks, and volumes. Then, with a single command, you create and start all the services from your configuration.

### Key Features of Docker Compose:
- **Service Definition**: Define multiple services (containers) in a single YAML file
- **Networking**: Automatic network creation between services
- **Dependency Management**: Control startup order with `depends_on`
- **Environment Management**: Easy configuration of environment variables
- **Volume Management**: Persistent data storage across container restarts

## Why Do We Need Docker Compose?

1. **Simplified Multi-Container Management**: Instead of running multiple `docker run` commands, manage all containers with one configuration file
2. **Environment Consistency**: Ensure the same environment across development, testing, and production
3. **Service Discovery**: Containers can communicate using service names instead of IP addresses
4. **Dependency Handling**: Automatically start services in the correct order
5. **Easy Scaling**: Scale services up or down with simple commands
6. **Development Efficiency**: Quickly spin up entire application stacks for development

## Project Structure

```
├── app.py              # Flask application
├── Dockerfile          # Container configuration for Flask app
├── docker-compose.yml  # Multi-container orchestration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Application Overview

This application consists of two services:
- **Flask App**: A web server that displays visit counts
- **Redis**: An in-memory database that stores the visit counter

### How It Works:
1. The Flask application connects to Redis using the service name `redis`
2. Each time you visit the homepage, the counter in Redis is incremented
3. The current count is displayed on the webpage

## Docker Compose Commands

### 1. `docker-compose up`

**Command**: `docker-compose up`

**What it does**:
- Looks for `docker-compose.yml` or `docker-compose.yaml` file in the current directory
- Reads and parses the compose configuration
- Builds images if they don't exist or have changed
- Creates and starts all defined services
- Creates a default network for service communication
- Streams logs from all containers to the terminal

**What happens when you run this**:
1. **File Discovery**: Docker Compose looks for `docker-compose.yml` (or `docker-compose.yaml`) in the current directory
2. **Configuration Parsing**: Reads and validates the YAML configuration file
3. **Network Creation**: Creates a bridge network (e.g., `docker_compose_default`)
4. **Image Building**: Builds the Flask app image using the Dockerfile
5. **Redis Container**: Pulls and starts the Redis Alpine image
6. **Flask Container**: Starts the Flask application container
7. **Service Communication**: Both containers can communicate using service names
8. **Port Mapping**: Maps container port 5000 to host port 5000
9. **Dependency Resolution**: Ensures Redis starts before the Flask app

**Example Output**:
```
Creating network "docker_compose_default" with the default driver
Building flask_app
Pulling redis
Creating docker_compose_redis_1 ... done
Creating docker_compose_flask_app_1 ... done
Attaching to docker_compose_redis_1, docker_compose_flask_app_1
```

### 2. `docker-compose up -d`

**Command**: `docker-compose up -d`

**What it does**:
- Same as `docker-compose up` but runs containers in detached mode (background)
- Returns control to the terminal immediately
- Containers continue running in the background

**What happens when you run this**:
1. All the same steps as `docker-compose up`
2. **Detached Mode**: Containers run in the background
3. **No Log Streaming**: Logs are not displayed in the terminal
4. **Terminal Control**: You can continue using the terminal for other commands

### 3. `docker-compose down`

**Command**: `docker-compose down`

**What it does**:
- Stops and removes all containers defined in the compose file
- Removes the created network
- Does NOT remove volumes or images by default

**What happens when you run this**:
1. **Container Stopping**: Gracefully stops all running containers
2. **Container Removal**: Removes the stopped containers
3. **Network Cleanup**: Removes the created network
4. **Service Cleanup**: Cleans up all resources except volumes and images

**Example Output**:
```
Stopping docker_compose_flask_app_1 ... done
Stopping docker_compose_redis_1 ... done
Removing docker_compose_flask_app_1 ... done
Removing docker_compose_redis_1 ... done
Removing network docker_compose_default
```

### 4. `docker-compose stop`

**Command**: `docker-compose stop`

**What it does**:
- Stops running containers without removing them
- Containers can be restarted later with `docker-compose start`
- Preserves container state and configuration

**What happens when you run this**:
1. **Graceful Shutdown**: Sends SIGTERM signal to containers
2. **Container Preservation**: Containers are stopped but not removed
3. **Network Preservation**: Network remains intact
4. **State Preservation**: Container state is preserved for restart

### 5. `docker-compose start`

**Command**: `docker-compose start`

**What it does**:
- Starts previously stopped containers
- Only works with containers that were stopped (not removed)
- Does not rebuild images or recreate containers

**What happens when you run this**:
1. **Container Restart**: Restarts stopped containers with preserved state
2. **Quick Startup**: Faster than `up` as no building/creating occurs
3. **State Recovery**: Containers resume from their previous state

### 6. `docker-compose restart`

**Command**: `docker-compose restart`

**What it does**:
- Restarts all services (stop + start)
- Useful for applying configuration changes
- Does not rebuild images

**What happens when you run this**:
1. **Stop Phase**: Gracefully stops all containers
2. **Start Phase**: Immediately starts the containers again
3. **Configuration Reload**: Applies any environment variable changes

### 7. `docker-compose logs`

**Command**: `docker-compose logs`

**What it does**:
- Shows logs from all services
- Can follow logs in real-time with `-f` flag
- Can specify specific services

**What happens when you run this**:
1. **Log Aggregation**: Collects logs from all containers
2. **Timestamped Output**: Shows logs with timestamps and service names
3. **Historical Data**: Shows logs since container creation

**Examples**:
```bash
docker-compose logs              # Show all logs
docker-compose logs -f           # Follow logs in real-time
docker-compose logs flask_app    # Show logs for specific service
```

### 8. `docker-compose ps`

**Command**: `docker-compose ps`

**What it does**:
- Shows the status of all services
- Displays container names, states, and port mappings

**What happens when you run this**:
1. **Status Check**: Queries Docker for container information
2. **Service Overview**: Shows which services are running/stopped
3. **Port Information**: Displays port mappings and exposed ports

### 9. `docker-compose build`

**Command**: `docker-compose build`

**What it does**:
- Builds or rebuilds images for services that have a `build` context
- Useful when you've made changes to Dockerfile or application code

**What happens when you run this**:
1. **Image Building**: Rebuilds images from Dockerfile
2. **Cache Utilization**: Uses Docker layer caching for efficiency
3. **Dependency Installation**: Reinstalls dependencies if requirements changed

## Getting Started

1. **Clone or download this project**

2. **Navigate to the project directory**:
   ```bash
   cd Docker_Compose
   ```

3. **Start the application**:
   ```bash
   docker-compose up
   ```

4. **Open your browser** and visit: `http://localhost:5000`

5. **See the counter increment** each time you refresh the page

6. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Troubleshooting

### Common Issues:

1. **Port Already in Use**:
   ```
   Error: Port 5000 is already in use
   ```
   **Solution**: Stop the service using port 5000 or change the port mapping in `docker-compose.yml`

2. **Redis Connection Failed**:
   ```
   redis.exceptions.ConnectionError
   ```
   **Solution**: Ensure Redis container is running and healthy with `docker-compose ps`

3. **Image Build Failures**:
   **Solution**: Run `docker-compose build --no-cache` to rebuild without cache

### Useful Debugging Commands:

```bash
# Check service status
docker-compose ps

# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs flask_app

# Execute commands in running container
docker-compose exec flask_app /bin/sh

# View networks
docker network ls

# Inspect the compose network
docker network inspect docker_compose_default
```

## Additional Docker Compose Options

### Environment Variables
You can override default values using environment variables:
```bash
# Set custom port
export PORT=8080
docker-compose up
```

### Scaling Services
```bash
# Run multiple instances of a service
docker-compose up --scale flask_app=3
```

### Production Deployment
```bash
# Run in production mode
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

This setup provides a solid foundation for understanding Docker Compose and building more complex multi-container applications!