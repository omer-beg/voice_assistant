from concurrent import futures  #futures helps to allow number of workers in server
import grpc
import protos.tts_pb2 as tts_pb2
import time
import protos.tts_pb2_grpc as tts_pb2_grpc
from style2_tts import app_style2

class TTSServiceServicer(tts_pb2_grpc.TTSServiceServicer):
    def __init__(self):
        start = time.time()
        print("Loading the StyleTTS2 model from server")
        app_style2.style_init()
        end = time.time()-start
        print("\nTotal model loading time is: "+ str(end)+" s\n")


    def Convert(self, request, context):
        print("Server Recieved Request")
        print(request)

        text = request.text
        
        # Process the text to generate speech
        result_path = app_style2.style_model(text)
        
        with open(result_path, 'rb') as f:
            audio_data = f.read()
        
        response = tts_pb2.ConvertResponse(audio=audio_data) 
        return response

def serve():
    options = [     #increase the message length to 10MB (standard is 4MB)
    ('grpc.max_receive_message_length', 10 * 1024 * 1024),  
    ('grpc.max_send_message_length', 10 * 1024 * 1024),    
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)    # max 10 workers alowed
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSServiceServicer(), server) #add service to server
    server.add_insecure_port('[::]:5053')  # grpc port
    server.start()  # start the server
    print("STARTING THE SERVER")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


