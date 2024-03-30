import http.server
import socketserver
import socket
import threading
import json
from datetime import datetime

# Configuration for the HTTP server address and port
HOST = '127.0.0.1'
PORT_HTTP = 3000

# Configuration for the Socket server address and port
SOCKET_HOST = '127.0.0.1'
PORT_SOCKET = 5000

# Class to handle HTTP requests
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handling static resources
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Class to handle the Socket server
class SocketServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        # Creating the Socket server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((SOCKET_HOST, PORT_SOCKET))
            print("Socket server started on {}:{}".format(SOCKET_HOST, PORT_SOCKET))
            
            while True:
                # Receiving data
                data, address = server_socket.recvfrom(1024)
                data_dict = json.loads(data.decode())
                data_dict["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                
                # Writing data to a JSON file
                with open('storage/data.json', 'a') as file:
                    json.dump(data_dict, file)
                    file.write('\n')

# Function to start the HTTP server
def start_http_server():
    with socketserver.TCPServer((HOST, PORT_HTTP), MyHttpRequestHandler) as httpd:
        print("HTTP server started on {}:{}".format(HOST, PORT_HTTP))
        httpd.serve_forever()

# Function to start the Socket server
def start_socket_server():
    socket_server = SocketServer()
    socket_server.start()

if __name__ == "__main__":
    # Starting servers in separate threads
    http_server_thread = threading.Thread(target=start_http_server)
    socket_server_thread = threading.Thread(target=start_socket_server)

    http_server_thread.start()
    socket_server_thread.start()

    http_server_thread.join()
    socket_server_thread.join()