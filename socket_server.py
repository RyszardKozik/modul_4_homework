import socket
import json
from datetime import datetime

# Define the address and port for the socket server
HOST = 'localhost'
PORT = 5000

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    print(f"Socket server listening on {HOST}:{PORT}")

    # Receive data from clients and process it
    while True:
        # Receive data from client
        data, address = server_socket.recvfrom(1024)
        
        # Decode JSON data
        message = json.loads(data.decode('utf-8'))
        
        # Add timestamp to the message
        message['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        # Update data.json file with the received message
        with open('storage/data.json', 'a') as file:
            json.dump(message, file)
            file.write('\n')