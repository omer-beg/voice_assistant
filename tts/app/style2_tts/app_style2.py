from style2_tts.StyleTTS2 import tts_new  
import logging
import time

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    filename='tts.log', 
    filemode='w' 
)

tts = None

def style_init():
    global tts
        # Initialize TTS model
    model_checkpoint_path = 'style2_tts/Models/LibriTTS/epochs_2nd_00020.pth'
    config_path = 'style2_tts/Models/LibriTTS/config.yml'

    logging.info("Creating the StyleTTS2 object")
    tts = tts_new.StyleTTS2(model_checkpoint_path, config_path)
    logging.info("Object created")



def style_model(text):
    start = time.time()
    global tts
    output_file = "output.wav"

    logging.info("Calling the inference function")
    tts.inference(
        text,
        target_voice_path="style2_tts/StyleTTS2/Demo/reference_audio/Vinay.wav",
        output_wav_file="output.wav",
        output_sample_rate=24000,
        alpha=0.2,
        beta=0.8, 
        diffusion_steps=10,  
        embedding_scale=1.2
    )
    logging.info("Inference function completed")
    end = time.time()-start
    logging.info("Total inference time is: "+ str(end)+" s")
    logging.info("\n\n")
   
    return output_file


