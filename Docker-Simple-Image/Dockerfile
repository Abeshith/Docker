FROM ubuntu:22.04

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py .

# Install Python dependencies
RUN pip3 install flask

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["python3", "app.py"]
