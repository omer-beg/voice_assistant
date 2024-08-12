import grpc
import model_service_pb2
import model_service_pb2_grpc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from concurrent import futures


class ModelService(model_service_pb2_grpc.ModelServiceServicer):
   def __init__(self):
       self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
       try:
           self.model = AutoModelForCausalLM.from_pretrained(
               "microsoft/Phi-3-mini-4k-instruct",
               torch_dtype="auto",
               trust_remote_code=True,
           )
           self.model.to(self.device)
       except RuntimeError as e:
           print(f"Error loading model: {e}")
           self.device = torch.device('cpu')
           self.model = AutoModelForCausalLM.from_pretrained(
               "microsoft/Phi-3-mini-4k-instruct",
               torch_dtype="auto",
               trust_remote_code=True,
           )
           self.model.to(self.device)


       self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
       self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if self.device.type == 'cuda' else -1)
  
   def GenerateText(self, request, context):
       input_text = request.input_text.strip()
       conversation_history = request.conversation_history.strip()


       # Format the prompt with clear delineation between user and assistant
       if conversation_history:
           combined_input = f"{conversation_history}\nUser: {input_text}\nAssistant:"
       else:
           combined_input = f"User: {input_text}\nAssistant:"


       generation_args = {
           "max_new_tokens": 150,  # Increased to give the assistant more space to complete responses
           "return_full_text": False,
           "temperature": 0.7,
           "do_sample": True,
           "top_k": 50,
           "top_p": 0.9,
           "stop_sequence": "\n",  # To stop after Assistant finishes speaking
       }


       try:
           with torch.cuda.amp.autocast(enabled=self.device.type == 'cuda'):
               output = self.pipe(combined_input, **generation_args)
           response_text = output[0]['generated_text'].strip()


           # Ensure that only the assistant's response is returned
           response_text = response_text.split("Assistant:")[-1].strip()
       except RuntimeError as e:
           response_text = f"Error: {e}"


       # Update conversation history for the next interaction
       new_conversation_history = conversation_history + f"\nUser: {input_text}\nAssistant: {response_text}"


       return model_service_pb2.GenerateTextResponse(
           generated_text=response_text,
           conversation_history=new_conversation_history
       )






def serve():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   model_service_pb2_grpc.add_ModelServiceServicer_to_server(ModelService(), server)
   server.add_insecure_port('[::]:50051')
   server.start()
   server.wait_for_termination()


if __name__ == '__main__':
   serve()


