import os
import sys
import grpc
import whisper
import tempfile
import time
import logging
from concurrent import futures

# Add the base directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'stt', 'app')))

from protos import stt_service_pb2 
from protos import stt_service_pb2_grpc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename=os.path.join(os.path.abspath(os.path.join(os.getcwd())), 'sttlog.log'),
    filemode='w'
)
global model_path
# Initialize Whisper model
model_path = os.path.join(os.getcwd(),'models', 'base.pt')
model = None

def load_model():
    global model
    starttime = time.time()
    try:
        logging.info("We are starting")
        if os.path.exists(model_path):
            logging.info(f"Model file found at {model_path}")
            model = whisper.load_model(model_path)
            logging.info("Whisper model loaded successfully")
            loadtime = time.time() - starttime
            logging.info(f"Time taken to load {loadtime}")
        else:
            logging.error(f"Model file not found at {model_path}")
            model = None
    except Exception as e:
        model = None
        logging.error(f"Error loading Whisper model: {e}")

class STTService(stt_service_pb2_grpc.STTServiceServicer):
    
    def ConvertSpeechToText(self, request, context):
        audio_data = request.audio
        temp_audio_file_path = None

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name
            logging.info(f"Temporary audio file path is {temp_audio_file_path} seconds")

        try:
            # Transcribe audio using Whisper
            starttime = time.time()
            result = None
            result = model.transcribe(temp_audio_file_path, fp16=False)
            logging.info(f"Transcription result: {result}")
            text = None
            logging.info(f"1 Detected text before new input: {text}")
            text = result.get("text", "")
            logging.info(f"2 Detected text: {text}")

            transcribetime = time.time() - starttime
            logging.info(f"Time taken to transcribe: {transcribetime} seconds")

            # Translate audio using Whisper by specifying the 'translate' task in transcribe
            starttime = time.time()
            translation_result = model.transcribe(temp_audio_file_path, task="translate", fp16=False)
            translation = translation_result.get("text", "")

            translatetime = time.time() - starttime
            logging.info(f"Time taken to translate: {translatetime} seconds")

            # Print the detected language
            detected_language = result['language']
            logging.info("Speech-to-text conversion successful")

            response = stt_service_pb2.SpeechResponse(
                message='Speech-to-text and translation successful',
                text=text,
                language=detected_language,
                translation=translation
            )
        
        except Exception as e:
            logging.error(f"Error converting speech to text: {e}")
            response = stt_service_pb2.SpeechResponse(
                error='Error converting speech to text',
                message=str(e)
            )

        finally:
            # Clean up
            if os.path.exists(temp_audio_file_path):
                os.remove(temp_audio_file_path)
                logging.info(f"Temporary audio file deleted: {temp_audio_file_path}")

        
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stt_service_pb2_grpc.add_STTServiceServicer_to_server(STTService(), server)
    server.add_insecure_port('[::]:5051')
    server.start()
    logging.info("gRPC server for stt started on port 5051")
    server.wait_for_termination()

if __name__ == '__main__':
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Load the Whisper model before starting the gRPC server
    load_model()
    serve()
