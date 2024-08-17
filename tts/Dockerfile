# Use the official Python slim image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /

# Install build tools, and protobuf compiler
RUN apt-get update && apt-get install -y \
    build-essential \
    protobuf-compiler \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
#Installing git
RUN apt-get update && apt-get install -y git


# Copy the application files
COPY . .

# Install all the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose the gRPC server port to the outside world
EXPOSE 50052

# Set environment variable for UTF-8 encoding
ENV PYTHONIOENCODING=utf-8

# Set the working directory
WORKDIR /app

# Run server.py when the container launches
CMD ["python3", "server.py"]
