# Speech-to-Text (STT) Service

## Overview

This repository contains a Speech-to-Text (STT) service built using OpenAI's Whisper models. The service is designed to transcribe speech from audio files into text and provides additional features such as language detection and translation. The service is implemented with gRPC and includes robust logging and telemetry for monitoring and debugging.

## Features

- **Speech-to-Text Conversion**: Transcribe audio files to text using Whisper's pre-trained models.
- **Language Detection**: Automatically detect the language of the input speech.
- **Translation**: Translate the detected language into English if the language is not English.
- **gRPC Endpoints**: Exposes gRPC endpoints for interaction with the STT service.
- **Logging**: Comprehensive logging for all operations including model loading, request handling, and error reporting.
- **Telemetry**: Tracks time taken for model loading, speech transcription, and translation.

## Prerequisites

- Python 3.x
- `grpcio`
- `grpcio-tools`
- `torch`
- `whisper`
- `protobuf`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo
   cd stt
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and place the Whisper model file in the `models` directory:
   - You can use any model just have to change the model name in stt/server.py.
   - By default the model used is `base.pt` Ensure you have downloaded and placed it in `models` directory.

## Usage

### Running the STT Service

1. Start the gRPC server:
   ```bash
   cd stt/app
   python server.py
   ```

2. The server will start on port `5051` by default. You can access the gRPC endpoints at `[::]:5051`.

### gRPC Endpoints

- **ConvertSpeechToText**: Accepts audio data and returns the transcribed text, detected language, and translation if applicable.

### Example gRPC Client

To interact with the STT service, you can use a gRPC client. Below is an example in Python:

```python
import grpc
from protos import stt_service_pb2
from protos import stt_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:5051') as channel:
        stub = stt_service_pb2_grpc.STTServiceStub(channel)
        with open('path_to_audio_file.wav', 'rb') as audio_file:
            audio_data = audio_file.read()

        request = stt_service_pb2.SpeechRequest(audio=audio_data)
        response = stub.ConvertSpeechToText(request)
        print("Text:", response.text)
        print("Detected Language:", response.language)
        print("Translation:", response.translation)

if __name__ == '__main__':
    run()
```

### Logging

Logs are stored in `sttlog.log` in the root directory. The log captures:

- Model loading times and status.
- gRPC request handling.
- Time taken for transcription and translation.
- Errors and exceptions.

## Telemetry

The service logs the following telemetry data:

- Time taken to load the Whisper model.
- Time taken for speech-to-text conversion.
- Time taken for translation.

This data is logged for performance monitoring and can be found in the `sttlog.log` file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

