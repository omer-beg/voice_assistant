# Bot Service

## Overview

This repository contains a Bot Service that leverages a language model to generate text responses based on user inputs. The service uses Hugging Face's transformers library and supports gRPC for communication. It includes features like GPU utilization, logging, and response generation customization.

## Features

- **Text Generation**: Generates contextual responses based on user inputs and conversation history.
- **gRPC Endpoints**: Exposes gRPC endpoints for interaction with the bot service.
- **GPU Utilization**: Automatically detects and utilizes available GPUs for faster text generation.
- **Logging**: Comprehensive logging for monitoring model loading, request handling, and error reporting.
- **Customizable Responses**: Allows setting parameters like temperature, top_k, and top_p for controlling text generation.

## Prerequisites

- Python 3.x
- `grpcio`
- `grpcio-tools`
- `torch`
- `transformers`
- `protobuf`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd bot/app
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that the model and tokenizer files are downloaded and available.

## Usage

### Running the Bot Service

1. Start the gRPC server:
   ```bash
   cd bot/app
   python server.py
   ```

2. The server will start on port `5052` by default. You can access the gRPC endpoints at `[::]:5052`.

### gRPC Endpoints

- **GenerateText**: Accepts user input text and conversation history, and returns a generated response along with updated conversation history.

### Example gRPC Client

To interact with the Bot Service, you can use a gRPC client. Below is an example in Python:

```python
import grpc
from protos import bot_service_pb2
from protos import bot_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:5052') as channel:
        stub = bot_service_pb2_grpc.ModelServiceStub(channel)
        request = bot_service_pb2.GenerateTextRequest(input_text="Hello, how are you?", conversation_history="")
        response = stub.GenerateText(request)
        print("Generated Text:", response.generated_text)
        print("Updated Conversation History:", response.conversation_history)

if __name__ == '__main__':
    run()
```

### Logging

Logs are stored in `botlog.log` in the root directory. The log captures:

- Model loading and GPU allocation details.
- gRPC request handling.
- Text generation output and errors.

## Configuration

### GPU Configuration

The service attempts to utilize available GPUs for text generation. It logs the available memory on each GPU and selects one with sufficient free memory. If no GPU is available, the service falls back to CPU.

### Text Generation Parameters

The text generation can be customized using the following parameters:
- **max_new_tokens**: Maximum number of new tokens to generate.
- **temperature**: Controls the randomness of predictions by scaling the logits before applying softmax.
- **top_k**: Limits the sampling pool to the top k logits.
- **top_p**: Cumulative probability threshold for nucleus sampling.

These parameters can be adjusted in the `GenerateText` method.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
