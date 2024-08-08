# python -m grpc_tools.protoc -I=protos --python_out=stt/app --grpc_python_out=stt/app protos/stt_service.proto
# python -m grpc_tools.protoc -I=protos --python_out=bot/app --grpc_python_out=bot/app protos/bot_service.proto
# python -m grpc_tools.protoc -I=protos --python_out=app --grpc_python_out=app protos/coordinator_service.proto

#!/bin/bash

# Free ports
echo "All ports free..."
python free_port.py &

# Start STT service
echo "Starting STT service..."
python stt/app/server.py &

# Start Bot service
echo "Starting Bot service..."
python bot/app/server.py &

# Start Coordinator service and Flask server
echo "Starting Coordinator service and Flask server..."
python server.py &

# Wait for all background processes to finish
wait
