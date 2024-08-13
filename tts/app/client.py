import grpc
from protos import tts_pb2
from protos import tts_pb2_grpc

def main():

    while True:
        text = input("Enter a string (or 'exit' to quit): ")

        if text.lower() == "exit":
            print("Exiting...")  
            break
        
        options = [     #increase the message length to 10MB (standard is 4MB)
        ('grpc.max_receive_message_length', 10 * 1024 * 1024),  
        ('grpc.max_send_message_length', 10 * 1024 * 1024),     
        ]
        # Connect to gRPC server
        with grpc.insecure_channel('localhost:50052', options=options) as channel:   #channel to connect to grpc
            stub = tts_pb2_grpc.TTSServiceStub(channel) # to call the function
            response = stub.Convert(tts_pb2.ConvertRequest(text=text))

        result_path = 'output.wav'
        with open(result_path, 'wb') as f:
            f.write(response.audio)

        print(f"Conversion complete. Audio saved to {result_path}")

if __name__ == "__main__":
    main()
