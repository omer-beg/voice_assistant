import grpc
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from concurrent import futures
import logging
from protos import bot_service_pb2
from protos import bot_service_pb2_grpc
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='botlog.log',
    filemode='w'
)

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
torch.cuda.empty_cache()

def get_available_gpu():
    for i in range(torch.cuda.device_count()):
        memory_free = torch.cuda.get_device_properties(i).total_memory / 1024**2 - torch.cuda.memory_reserved(i) / 1024**2
        logging.info(f"GPU {i}: {memory_free:.2f} MB free")
        if memory_free > 200:  # Check if free memory is greater than 200 MB
            return i
    return None  # No GPU with sufficient memory found

class BotService(bot_service_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        logging.info("Initializing BotService")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        available_gpu = get_available_gpu()
        if available_gpu is not None:
            self.device = torch.device(f'cuda:{available_gpu}')
            logging.info(f"Using GPU {available_gpu}")
        else:
            self.device = torch.device('cpu')
            logging.info("Using CPU")

        # Measure model loading time
        start_time = time.time()
        self.model = self.load_model()
        load_time = time.time() - start_time
        logging.info(f"Model loaded in {load_time:.2f} seconds")

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if self.device.type == 'cuda' else -1)
        logging.info("BotService initialized")

    def load_model(self):
        try:
            logging.info("Loading model")
            model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", torch_dtype="auto", trust_remote_code=True)
            if torch.cuda.device_count() > 1:
                model = torch.nn.DataParallel(model)
                logging.info("Using multiple GPUs")
            model.to(self.device)
            logging.info("Model loaded successfully")
        except RuntimeError as e:
            logging.error(f"Error loading model: {e}")
            self.device = torch.device('cpu')
            model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", torch_dtype="auto", trust_remote_code=True)
            model.to(self.device)
        return model

    def GenerateText(self, request, context):
        logging.info("Received GenerateText request")
        torch.cuda.empty_cache()

        input_text = request.input_text.strip()
        conversation_history = request.conversation_history.strip()

        combined_input = f"{conversation_history}\nUser: {input_text}\nAssistant:" if conversation_history else f"User: {input_text}\nAssistant:"
        
        generation_args = {
            "max_new_tokens": 100,
            "return_full_text": False,
            "temperature": 0.7,
            "do_sample": True,
            "top_k": 50,
            "top_p": 0.9,
            "stop_sequence": "\n",
        }

        try:
            # Measure text generation time
            start_time = time.time()
            output = self.pipe(combined_input, **generation_args)
            generation_time = time.time() - start_time
            logging.info(f"Text generation completed in {generation_time:.2f} seconds")

            response_text = output[0]['generated_text'].strip()
            logging.info(f"Generated response: {response_text}")
        except RuntimeError as e:
            logging.error(f"Error during text generation: {e}")
            response_text = "Error in generating response."

        response_text = response_text.replace("User:", "").strip()
        response_text = response_text.replace("Assistant:", "").strip()

        new_conversation_history = f"{conversation_history}\nUser: {input_text}\nAssistant: {response_text}"
        logging.info("Response Generation Successful\n\n")
        return bot_service_pb2.GenerateTextResponse(
            generated_text=response_text,
            conversation_history=new_conversation_history
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bot_service_pb2_grpc.add_ModelServiceServicer_to_server(BotService(), server)
    server.add_insecure_port('[::]:5052')
    server.start()
    logging.info("Server started on port 5052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
