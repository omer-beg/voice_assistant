from flask import Flask, request, send_file, jsonify
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, # (works for all levels above debug: info, warning, error,critical)
    format='%(asctime)s - %(levelname)s - %(message)s', # time stamp, level name, message to be displayed
    filename='app-tts.log', # file where log is saved
    filemode='w' # file created in write mode (overwrites existing file if present)
)

app = Flask(__name__)

# Path to the Piper binary and model
piper_binary = "./piper"
#model_path = "./voices/en_US-kathleen-low.onnx"
# skips over words: en_GB-southern_english_female-low.onnx"
## skips over words: en_US-danny-low.onnx", en_US-joe-medium.onnx better than southern

#model_path = "./voices/en_US-joe-medium.onnx"

output_file = "output.wav"

# directs root directory to the index.html page
@app.route('/')
def index():
    logging.info("Opening the index.html webpage")
    return app.send_static_file("index.html")

# Handle text-to-speech conversion
@app.route('/convert', methods=['POST', 'GET'])
def convert_text_to_speech():
    #POST METHOD
    if request.method == 'POST':
        selected_voice = request.form['voice']  # Get selected voice model
        text_to_convert = request.form['text']

        if not text_to_convert:
            logging.error("String not recieved")
        else:
            logging.info("Text recieved, proceeding to conversion")                   
    
        try:
            # Determine model path based on selected voice
            if selected_voice == "en_US-joe-medium":
                model_path = "./voices/en_US-joe-medium.onnx"
            elif selected_voice == "en_US-danny-low":
                model_path = "./voices/en_US-danny-low.onnx"
            elif selected_voice == "en_US-kathleen-low":
                model_path = "./voices/en_US-kathleen-low.onnx"
            elif selected_voice == "en_GB-southern_english_female-low":
                model_path = "./voices/en_GB-southern_english_female-low.onnx"
            else:
                logging.error(f"Unknown voice selected: {selected_voice}")
                return jsonify({'error': 'Unknown voice selected'}), 400
            logging.info(f"voice model selected: {selected_voice}")
            
            logging.info("Processing the input textual string")
            # Convert text to speech using Piper TTS
            subprocess.run(
                [piper_binary, "-m", model_path, "-f", output_file],
                input=text_to_convert.encode('utf-8'),  # encode textual string to 8 bit code (requirement to run subprocesses)
                check=True  # for error checking, raises exception in case of if failure of subprocess call
            )
            logging.info("Conversion complete")
        
            # Return the audio file
            logging.info("Returning the generated audio to the webpage")
            return send_file(output_file, mimetype='audio/wav', as_attachment=False)

        except Exception as e:
            logging.error("Error converting text to speech --tts.py")
            return jsonify({'error': f'Error converting text to speech(json): {str(e)}'}), 500

    # GET METHOD
    # not needed remove later (for old index.html)
    elif request.method == 'GET':
        # Serve the audio file for playback
        logging.info("Audio file returned to GET call")
        return send_file(output_file, mimetype='audio/wav')
        


# Main function to run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=55000)