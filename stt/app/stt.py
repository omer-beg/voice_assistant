from flask import Flask, request, jsonify, send_from_directory
import whisper
import os
import sys
import tempfile
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='sttlog.log',
    filemode='w'
)


app = Flask(__name__)

# Initialize Whisper model
try:
    logging.info(f"We are starting")
    model_path = os.path.join(os.getcwd(), 'models', 'base.pt')
    logging.info(f"Model file is at {model_path}")
    if os.path.exists(model_path):
        logging.info(f"Model file found at {model_path}")

        model = whisper.load_model(model_path)
        print("Whisper model loaded successfully")
        logging.info("Whisper model loaded successfully")
    else:
        logging.error(f"Model file not found at {model_path}")
        print(f"Model file not found at {model_path}")
        model = None

except Exception as e:
    model = None
    logging.error(f"Error loading Whisper model: {e}") 
    print("Error loading Whisper model")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/speech-to-text', methods=['POST'])
def convert_speech_to_text():
    if 'audio' not in request.files:
        logging.info(f"Audio file is missing")
        print("Audio file is missing")
        return jsonify({'error': 'Audio file is missing'}), 400
    
    else:
        audio_file = request.files['audio']
        #logging.info(f"audio File has {audio_file}")
        print("Audio file received")
        logging.info(f"Audio file is {audio_file.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        audio_file.save(temp_audio_file.name)
        temp_audio_file_path = temp_audio_file.name
        logging.info(f"Temporary audio file path is {temp_audio_file_path}")
        print("Temporary Audio file")
        
    try:
        # Transcribe audio using Whisper
        result = model.transcribe(temp_audio_file_path,fp16=False)
        text = result.get("text", "")
        logging.info(f"Speech-to-text conversion successful")
        print("Speech-to-text conversion successful")
        return jsonify({'message': 'Speech-to-text conversion successful', 'text': text})

    except Exception as e:
        print(f"Error converting speech to text: {e}")
        logging.info(f"Error converting speech to text: {e}")
        return jsonify({'error': 'Error converting speech to text'}), 500
'''
    finally:
        # Clean up
        if os.path.exists(temp_audio_file_path):
            os.remove(temp_audio_file_path)
'''

if __name__ == '__main__':
    # Change default encoding to UTF-8
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout.reconfigure(encoding='utf-8')
    app.run(debug=True, host='0.0.0.0', port=55500)
