# Docker Multistage Build with Distroless Images

This repository demonstrates Docker multistage builds using Google's distroless base images for Python applications.

## What is Multistage Build?

Multistage builds allow you to use multiple `FROM` statements in a single Dockerfile. Each `FROM` instruction can use a different base image, and you can selectively copy artifacts from one stage to another. This approach helps create smaller, more secure production images by:

- **Reducing image size**: Only the necessary runtime files are included in the final image
- **Improving security**: Removes build tools, package managers, and other unnecessary components
- **Better caching**: Each stage can be cached independently

## What are Distroless Images?

Distroless images are minimal base images that contain only your application and its runtime dependencies. They don't include:
- Package managers (apt, yum, etc.)
- Shells (bash, sh)
- Network tools
- Text editors
- Most GNU coreutils

### Benefits of Distroless Images:
- **Smaller attack surface**: Fewer components mean fewer vulnerabilities
- **Reduced image size**: Typically 2-10x smaller than traditional base images
- **Better security**: No shell access reduces attack vectors
- **Compliance**: Easier to meet security compliance requirements

## When to Use Distroless Images

### ✅ Use Distroless When:
- Building production applications
- Security is a primary concern
- You want minimal image sizes
- Applications don't require debugging tools in production
- Following microservices architecture

### ❌ Avoid Distroless When:
- During development (debugging is difficult)
- Applications require shell access
- Need to install packages at runtime
- Legacy applications with complex dependencies

## Dockerfile Workflow Explained

```dockerfile
## Stage 1: Builder Stage
FROM python:3.9 AS builder
WORKDIR /app
COPY calculator.py .

## Stage 2: Production Stage
FROM gcr.io/distroless/python3
WORKDIR /app
COPY --from=builder /app/calculator.py .
CMD ["calculator.py"]
```

### Stage 1 (Builder):
1. Uses full Python 3.9 image with all build tools
2. Sets working directory to `/app`
3. Copies the Python application file
4. Tagged as `builder` for reference in later stages

### Stage 2 (Production):
1. Uses Google's distroless Python3 base image
2. Sets working directory to `/app`
3. Copies only the application file from the builder stage
4. Sets the command to run the Python script

## Size Comparison

| Image Type | Approximate Size |
|-----------|------------------|
| python:3.9 | ~885 MB |
| python:3.9-slim | ~122 MB |
| gcr.io/distroless/python3 | ~51 MB |

## How to Build and Run

### Build the Docker image:
```bash
docker build -t calculator-distroless .
```

### Run the container:
```bash
docker run calculator-distroless
```

Expected output:
```
Sum: 8
```

## Available Distroless Images

Visit the [Google Container Tools Distroless repository](https://github.com/GoogleContainerTools/distroless) for more distroless base images:

- `gcr.io/distroless/java`: Java applications
- `gcr.io/distroless/python3`: Python 3 applications
- `gcr.io/distroless/nodejs`: Node.js applications
- `gcr.io/distroless/go`: Go applications (static binaries)
- `gcr.io/distroless/cc`: C/C++ applications

## Key Takeaways

- Multistage builds separate build-time and runtime dependencies
- Distroless images provide minimal, secure runtime environments
- Perfect for production deployments where security and size matter
- Development should still use full-featured base images for debugging capabilities