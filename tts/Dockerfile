FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# this copies the piper module into the docker container
COPY . /app

# try using a virtual env


# expose the port
EXPOSE 55000

# Install dependencies
RUN pip install --no-cache-dir Flask pygame

#run the application
CMD ["python3", "app.py"]