# Text-to-Speech (TTS) Service

This repository contains the implementation of a Text-to-Speech (TTS) model based on the [StyleTTS2](https://github.com/yl4579/StyleTTS2) model. The TTS model converts input text into speech, leveraging the advanced neural architecture of StyleTTS2 for high-quality audio generation. This README provides an overview of the project, including the installation requirements and a basic explanation of how the model works.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [GRPC Endpoints](#grpc-endpoints)
- [Model Architecture](#model-architecture)
- [Docker Deployment](#docker-deployment)
- [License](#license)
- [Notes](#notes)

## Overview

The TTS model implemented in this project uses the StyleTTS2 architecture to synthesize speech from text input. StyleTTS2 is a state-of-the-art model known for its ability to generate high-fidelity and natural-sounding speech. This implementation allows for flexible and efficient text-to-speech conversion, with potential applications in voice assistants, audiobooks, and other speech-enabled systems.

### Key Features:
- **High-Quality Speech Generation**: The model produces clear and natural-sounding speech.
- **GPU Acceleration**: Leverages NVIDIA GPUs for efficient inference.
- **Modular Architecture**: Easy to integrate and modify for various use cases.

## Requirements

To set up and run the TTS model, the following software and libraries are required:

- **Operating System**: Linux (tested on Ubuntu, Linux Mint), Windows
- **Python**: Version 3.8 or higher
- **CUDA**: Version 11.0 or higher (for GPU acceleration)
- **PyTorch**: Version 1.10 or higher
- **StyleTTS2**: [StyleTTS2 Repository](https://github.com/yl4579/StyleTTS2)

### Python Libraries:

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation:

1. Clone the repository:
```bash
https://github.com/yl4579/StyleTTS2
```
2. Install Dependencies:

    Ensure that all required libraries are installed:
3. Download the pretrained model:
```bash
https://huggingface.co/yl4579/StyleTTS2-LibriTTS/tree/main
```
or any other model of your choice.

4. Download an audio file:
```bash
https://huggingface.co/yl4579/StyleTTS2-LibriTTS/resolve/main/reference_audio.zip
```
5. Configure the Environment:

Set up the environment variables and CUDA paths if necessary.

## Usage:

Once the installation is complete, you can run the TTS model using the provided scripts.

```bash
python service.py 
python client.py
```
Run both the code files in seperate terminals. Input the text string in the client terminal. An audio file is generated as a response.

## GRPC Endpoints:
Run the tts.protos file to genertate GRPC code using the following command:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tts.proto
```
## Model Architecture:

The StyleTTS2 model is built upon a neural network architecture that combines a variational autoencoder (VAE) with attention mechanisms to produce high-quality speech. The model includes:

- Text Encoder: Converts text into a phoneme-based representation.
- Style Encoder: Captures prosody and style variations in the speech.
- Decoder: Synthesizes the speech from the encoded text and style information.

## Docker Deployment:

Run the following commands to built and run the docker image.
```bash
docker build -t imageName .
docker run p 5003:5003 --name containerName -i imageName:tag
```
## License:
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Notes:

### Useful docker commands:
```bash
docker logs <container_id> (to view logs/error messages)
docker ps (to view all the running containers)
docker images (to view all the built images)
docker stop <container_id> (to stop a running container)
docker exec <container_id_or_name> /bin/bash (to enter a running container)
```
### Future Updates:
- Integrate GPU so it can work on multiple GPUs at once.
- Train the StyleTTS2 model to process Urdu text.
