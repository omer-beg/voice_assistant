# Voice Assistant Microservices

## Overview

This repository contains a complete voice assistant built using microservices architecture. The project integrates three key services:

1. **Speech-to-Text (STT) Service**: Transcribes speech from audio files into text using OpenAI's Whisper models.
2. **Bot Service**: Generates contextual text responses based on user inputs using Microsoft PHI-3 mini.
3. **Text-to-Speech (TTS) Service**: Converts text responses back into speech using Style2 TTS.

The services communicate with each other using gRPC, and the coordinator service orchestrates the workflow. A Flask-based web interface allows users to interact with the voice assistant.

## Features

- **Speech-to-Text**: Converts audio input to text with language detection and optional translation.
- **Text Generation**: Produces contextual responses using a language model with customizable parameters.
- **Text-to-Speech**: Converts text responses to speech and returns audio files.
- **gRPC Communication**: Microservices interact using gRPC for efficient, scalable communication.
- **Web Interface**: Users can interact with the assistant via a simple web page.
- **Logging and Telemetry**: Comprehensive logging and performance monitoring for all services.

## Prerequisites

- Python 3.x
- Docker (for containerizing the services)
- Required Python packages (`grpcio`, `grpcio-tools`, `torch`, `transformers`, `gTTS`, etc.)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/voice-assistant.git
   cd voice-assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Models**:
   - Download and place the Whisper model in the `stt/models` directory.
   - Ensure the Hugging Face model and tokenizer files are available for the bot service.

## Running the Services

### 1. Start the Speech-to-Text (STT) Service

```bash
cd stt/app
python server.py
```
- This service will run on port 5051 by default.

### 2. Start the Bot Service

```bash
cd bot/app
python server.py
```
- This service will run on port 5052 by default.

### 3. Start the Text-to-Speech (TTS) Service

```bash
cd tts/app
python server.py
```
- This service will run on port 5053 by default.

### 4. Start the Coordinator Service

```bash
cd coordinator
python server.py
```
- The Flask web interface will be available on port 8080 by default.

## Web Interface

The web interface allows users to interact with the voice assistant. Users can:

1. Record their voice or upload an audio file.
2. The audio is sent to the STT service for transcription.
3. The transcribed text (or its translation) is sent to the bot service for generating a response.
4. The bot's response is converted to speech using the TTS service.
5. The audio playback is presented on the web page.

## gRPC Endpoints

### Speech-to-Text Service

- **ConvertSpeechToText**: Accepts audio data and returns transcribed text, detected language, and translation.

### Bot Service

- **GenerateText**: Accepts text and conversation history, and returns a generated response along with updated conversation history.

### Text-to-Speech Service

- **ConvertTextToSpeech**: Accepts text and returns the corresponding audio data.

## Logging and Telemetry

Each service maintains its own log file, capturing detailed information:

- **STT Service**: Logs model loading, transcription, language detection, and translation details.
- **Bot Service**: Logs text generation parameters, response times, and errors.
- **TTS Service**: Logs text-to-speech conversion and any errors.

Telemetry data, including time taken for various operations, is also logged for performance monitoring.

## Deployment

### Docker

You can deploy the entire system using Docker:

1. **Build the Docker Images**:
   ```bash
   docker-compose build
   ```

2. **Run the Containers**:
   ```bash
   docker-compose up
   ```

3. **Access the Web Interface**:
   Open your browser and navigate to `http://localhost:8080`.

### Cloud Deployment

To deploy on a cloud platform (AWS, GCP, Azure), push your Docker images to a Docker registry and configure your cloud services to run the containers.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
