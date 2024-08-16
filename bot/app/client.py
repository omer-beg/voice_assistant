import grpc
from protos import bot_service_pb2
from protos import bot_service_pb2_grpc
from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_response(input_text, conversation_history):
    # Create a gRPC channel and stub
    channel = grpc.insecure_channel('localhost:5052')
    stub = bot_service_pb2_grpc.ModelServiceStub(channel)
  
    # Create a request
    grpc_request = bot_service_pb2.GenerateTextRequest(
        input_text=input_text,
        conversation_history=conversation_history
    )
  
    # Make the call
    try:
        response = stub.GenerateText(grpc_request)
        return response.generated_text, response.conversation_history
    except grpc.RpcError as e:
        return f"gRPC error: {e}", conversation_history

@app.route('/get-response', methods=['POST'])
def upload_request():
    # Parse JSON request body
    data = request.get_json()
    input_text = data.get('input_text')
    conversation_history = data.get('conversation_history')
    
    if not input_text or not conversation_history:
        return jsonify({"error": "Missing input_text or conversation_history"}), 400
    
    # Get response from gRPC service
    generated_text, updated_history = generate_response(input_text, conversation_history)
    
    # Prepare and return JSON response
    result = {
        "generated_text": generated_text,
        "conversation_history": updated_history
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
