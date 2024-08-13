Speech-to-Text Flask Application
This Flask application converts speech audio input to text using the Whisper model.

Prerequisites
Before running the application, ensure you have the following installed:

Python 3.x
Flask
Whisper
PortAudio
Installation
Follow these instructions to set up the working environment:

Clone the Repository
git clone https://github.com/arrij46/STT_Microservice.git
cd STT_Microservice
Install the dependencies
pip install -r requirements.txt
The requirements.txt includes:

Flask
whisper
pyaudio
requests
Install System Dependencies
For the application to work correctly, you need to install the following system dependencies:

For Windows: You might need to install PortAudio binaries and set up PyAudio.
For Linux:
sudo apt-get update
sudo apt-get install -y portaudio19-dev ffmpeg
Usage
Run the Flask application:
For Windows:
python app/stt.py
For Linux:
python3 app/stt.py
Open your web browser and navigate to http://localhost:55000/ to access the application.

Upload an audio file on the webpage and click "Convert".

The application will convert the speech in the audio file to text and display the result.

API Endpoints
/ - Homepage serving index.html for user interaction.
/api/speech-to-text - POST endpoint for converting speech to text. Accepts an audio file.
Method: POST
Parameters: audio (audio file to convert to text)
Returns: JSON response with the transcribed text.
Logging
Application logs are stored in app.log.
Log level is set to INFO, logging various stages of speech-to-text conversion.
Docker Deployment
To run the application using Docker:

Create a Dockerfile:
# Use the official Python slim image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pyaudio and other packages
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary packages
RUN pip install -r requirements.txt

# Copy the application files into the container
COPY app /app/app

# Set environment variable for UTF-8 encoding
ENV PYTHONIOENCODING=utf-8

# Specify the command to run on container start
CMD ["python", "app/stt.py"]
Build the Docker image:
docker build -t stt-app .
Run the Docker container:
docker run -p 55000:55000 stt-app
After running, open the local host at http://localhost:55000/ to test your application.
Notes
Ensure the Whisper model is correctly loaded in the application code.
The Flask application should be configured to handle file uploads and process them using the Whisper model for transcription.
