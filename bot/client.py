import grpc
import model_service_pb2
import model_service_pb2_grpc


def run():
   channel = grpc.insecure_channel('localhost:50051')
   stub = model_service_pb2_grpc.ModelServiceStub(channel)
  
   conversation_history = ""
  
   while True:
       user_input = input("You: ")
       if user_input.lower() in ["exit", "quit"]:
           break
      
       response = stub.GenerateText(model_service_pb2.GenerateTextRequest(
           input_text=user_input,
           conversation_history=conversation_history  # Ensure this field is correct
       ))
      
       print("Assistant: " + response.generated_text)
       conversation_history = response.conversation_history


if __name__ == '__main__':
   run()
