# Docker Simple Image

This folder contains a simple Flask application demonstrating basic Docker concepts and containerization.

## What is Docker?

Docker is a platform that uses containerization technology to package applications and their dependencies into lightweight, portable containers. It allows developers to create, deploy, and run applications consistently across different environments.

## What is a Container?

A container is a lightweight, standalone, and executable package that includes everything needed to run an application:
- Application code
- Runtime environment
- System tools and libraries
- Dependencies
- Configuration files

Containers are isolated from each other and the host system, ensuring consistent behavior regardless of where they run.

## Why Do We Need Docker Images?

Docker images are essential because they:
- **Consistency**: Ensure applications run the same way across different environments (development, testing, production)
- **Portability**: Allow applications to run on any system that supports Docker
- **Isolation**: Prevent conflicts between different applications and their dependencies
- **Efficiency**: Share common layers between images, reducing storage and transfer time
- **Scalability**: Enable easy scaling and deployment of applications

## What is a Dockerfile?

A Dockerfile is a text file containing a series of instructions that Docker uses to automatically build an image. It defines:
- The base operating system or runtime
- Dependencies and packages to install
- Application code to include
- Configuration settings
- Commands to run when the container starts

## Docker Commands Used in This Project

### FROM
```dockerfile
FROM ubuntu:22.04
```
- Specifies the base image to start building from
- In this case, we're using Ubuntu 22.04 as our foundation

### RUN
```dockerfile
RUN apt-get update && apt-get install -y python3 python3-pip
```
- Executes commands during the image build process
- Used to install packages, update system, or run setup scripts
- Each RUN command creates a new layer in the image

### WORKDIR
```dockerfile
WORKDIR /app
```
- Sets the working directory inside the container
- All subsequent commands will be executed from this directory
- Creates the directory if it doesn't exist

### COPY
```dockerfile
COPY app.py .
```
- Copies files or directories from the host machine to the container
- First argument: source path (on host)
- Second argument: destination path (in container)
- The `.` represents the current working directory (`/app`)

### EXPOSE
```dockerfile
EXPOSE 5000
```
- Documents which port the container will listen on at runtime
- Doesn't actually publish the port (that's done with `docker run -p`)
- Acts as documentation for users of the image

## Project Structure

```
Docker_Simple_Image/
├── app.py          # Simple Flask web application
├── Dockerfile      # Instructions to build the Docker image
└── README.md       # This documentation file
```

## How to Use This Example

1. **Build the Docker image:**
   ```bash
   docker build -t simple-flask-app .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 simple-flask-app
   ```

3. **Access the application:**
   Open your browser and visit `http://localhost:5000`

## Key Benefits Demonstrated

- **Environment Consistency**: The application runs the same way regardless of the host system
- **Dependency Management**: Python and Flask are installed automatically
- **Easy Deployment**: Anyone can run this application with just two Docker commands
- **Isolation**: The application runs in its own container, separate from the host system
