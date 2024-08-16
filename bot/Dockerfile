# Use the official Python slim image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /application

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy the requirements file and install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copy the application files, including the protos directory
COPY app/protos ./protos
COPY app/server.py .

# Expose the gRPC server port
EXPOSE 5052

# Set the environment variable for CUDA
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Run the gRPC server when the container launches
CMD ["python3", "server.py"]
