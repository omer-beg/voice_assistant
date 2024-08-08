import os
import sys
import grpc
from flask import Flask, request, jsonify
import tempfile

# Add the base directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'stt', 'app')))

from protos import stt_service_pb2 
from protos import stt_service_pb2_grpc

app = Flask(__name__)

def convert_speech_to_text(audio_data):
    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('localhost:5051')
    stub = stt_service_pb2_grpc.STTServiceStub(channel)

    # Create a request
    request = stt_service_pb2.SpeechRequest(audio=audio_data)

    # Make the call
    try:
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



@app.route('/speech-to-text', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file is missing'}), 400

    audio_file = request.files['audio']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        audio_file.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name

    try:
        with open(temp_audio_file_path, "rb") as f:
            audio_data = f.read()
        result = convert_speech_to_text(audio_data)
    finally:
        os.remove(temp_audio_file_path)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
