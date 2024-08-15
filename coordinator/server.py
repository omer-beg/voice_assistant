import grpc
import os
import time
import logging
from concurrent import futures

from bot.app.protos import bot_service_pb2 
from bot.app.protos import bot_service_pb2_grpc 
from tts.app.protos import tts_pb2 
from tts.app.protos import tts_pb2_grpc 
from stt.app.protos import stt_service_pb2
from stt.app.protos import stt_service_pb2_grpc 
from flask import Flask, request, jsonify, send_from_directory, send_file


app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='coordinatorlog.log',
    filemode='w'
)

def generate_response(input_text, conversation_history=""):
    # sets up a connection to a remote service running on the same computer on port 5052.
    channel = grpc.insecure_channel('localhost:5052')
    # creates a client to interact with the remote chatbot service
    stub = bot_service_pb2_grpc.ModelServiceStub(channel)
    # creating a request
    request = bot_service_pb2.GenerateTextRequest(input_text=input_text, conversation_history=conversation_history)
    try:
        response = stub.GenerateText(request)
        return response.generated_text, response.conversation_history
    
    except grpc.RpcError as e:
        return f"gRPC error: {e}", conversation_history

def get_bot_response(text):
    response_text, conversation_history = generate_response(text)
    if "gRPC error" in response_text:
        return {'error': response_text}
    else:
        return {'message': 'Response generated successfully', 'text': response_text, 'conversation_history': conversation_history}

def convert_speech_to_text(audio_data):
    # set up a connection with a remote service on port 5051
    channel = grpc.insecure_channel('localhost:5051')
    # client created to interact with the remote service
    stub = stt_service_pb2_grpc.STTServiceStub(channel)
    # prepare a request with the audio data
    request = stt_service_pb2.SpeechRequest(audio=audio_data)
    try:
        # send the request
        response = stub.ConvertSpeechToText(request)
        if response.error:
            return {'error': response.error}
        else:
            return {
                'message': response.message,
                'text': response.text,
                'language': response.language,
                'translation': response.translation
            }
    except grpc.RpcError as e:
        return {'error': f'gRPC error: {e}'}

def convert_text_to_speech(text):
    channel = grpc.insecure_channel('localhost:5053')
    stub = tts_pb2_grpc.TTSServiceStub(channel)
    request = tts_pb2.ConvertRequest(text=text)
    
    try:
        response = stub.Convert(request)
        return {'audio': response.audio}
    except grpc.RpcError as e:
        return {'error': f'gRPC error: {e}'}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/speech-to-text', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        logging.info("Audio file is missing")
        return jsonify({'error': 'Audio file is missing'}), 400
    else:
        logging.info("Audio file received")
        audio_data = request.files['audio'].read()
        starttime = time.time()
        result = None
        result = convert_speech_to_text(audio_data)
        
    if 'error' in result:
        logging.info("Error in stt transcription")
        return jsonify({'error': result['error']}), 500
    else:
        text = None
        text = result['text']
        language = result['language']
        translation = result['translation']
        logging.info("Speech-to-text conversion successful")
        loadtime = time.time() - starttime
        logging.info(f"Time taken to convert speech to text {loadtime}")

        # Sending the STT's response to bot
        starttime = time.time()
        if language == 'en':
            logging.info(f"Sending transcription to bot: {text}")
            bot_response = get_bot_response(text)
        else: 
            logging.info(f"Sending translation to bot: {text}")
            bot_response = get_bot_response(translation)

        if 'error' in bot_response:
            logging.info("Error in bot response generation")
            return jsonify({'error': bot_response['error']}), 500
        
        loadtime = time.time() - starttime
        logging.info(f"Time taken by bot {loadtime}")

        # Send the bot's response to the TTS service
        starttime = time.time()
        logging.info("Sending the response to TTS")
        tts_audio = convert_text_to_speech(bot_response['text'])
        if 'error' in tts_audio:
            logging.info("Error in TTS conversion")
            return jsonify({'error': tts_audio['error']}), 500
        
        logging.info("Text to speech Successful")
        loadtime = time.time() - starttime
        logging.info(f"Time taken by tts {loadtime}")

        logging.info("Returning response to web\n\n")
        return jsonify({
            'text': text,
            'bot_response': bot_response['text']
        })

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    logging.info("Starting Flask development server on port 8080")
    app.run(port=8080, debug=True, use_reloader=False)

'''
import subprocess
def run_subprocess(script_path):
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        logging.info(f"{script_path} running")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running {script_path}: {e.stderr}")

run_subprocess('stt/app/server.py')
run_subprocess('bot/app/server.py')
'''