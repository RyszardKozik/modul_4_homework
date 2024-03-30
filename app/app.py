import http.server
import socketserver
import json
import socket
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus

# Define the request handler class
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Parse the POST data
        parsed_data = parse_qs(post_data.decode('utf-8'))
        username = parsed_data.get('username', [''])[0]
        message = parsed_data.get('message', [''])[0]
        
        # Send data to socket
        send_to_socket(username, message)
        
        # Send response
        self.send_response(HTTPStatus.FOUND)
        self.send_header('Location', '/')
        self.end_headers()

# Define function to send data to socket
def send_to_socket(username, message):
    data = {'username': username, 'message': message}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode('utf-8'), ('localhost', 5000))

# Define HTTP server parameters
host = 'localhost'
port = 8000

# Create and run the HTTP server
with socketserver.TCPServer((host, port), MyHttpRequestHandler) as httpd:
    print(f"HTTP server is running at http://{host}:{port}")
    httpd.serve_forever()
