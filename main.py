from datetime import datetime
import json
import socket
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Constants and configuration variables
SOCKET_IP = 'localhost'
SOCKET_PORT = 5000
HTTP_PORT = 3000
STORAGE_DIR = 'storage'
DATA_FILE = 'data.json'
STATIC_DIR = 'static'

# Jinja2 configuration
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

# HTTP request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = env.get_template('index.html')
            self.wfile.write(template.render().encode('utf-8'))
        elif self.path == '/message':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = env.get_template('message.html')
            self.wfile.write(template.render().encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        username = parsed_data['username'][0]
        message = parsed_data['message'][0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        send_to_socket({'username': username, 'message': message, 'timestamp': timestamp})
        update_data_json({'username': username, 'message': message, 'timestamp': timestamp})
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

# Function to update data JSON
def update_data_json(message):
    try:
        if not os.path.exists(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)

        data_file_path = os.path.join(STORAGE_DIR, DATA_FILE)

        if not os.path.exists(data_file_path):
            with open(data_file_path, 'w') as f:
                json.dump({}, f)

        with open(data_file_path, 'r+') as f:
            data = json.load(f)
            data[message['timestamp']] = {'username': message['username'], 'message': message['message']}
            f.seek(0)
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error updating data JSON: {e}")

# Function to send data to socket server
def send_to_socket(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps(data).encode('utf-8'), (SOCKET_IP, SOCKET_PORT))
    except Exception as e:
        print(f"Error sending data to socket server: {e}")

# Socket server function
def socket_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((SOCKET_IP, SOCKET_PORT))
            print(f'Socket server listening on port {SOCKET_PORT}')
            while True:
                data, addr = s.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                update_data_json(message)
    except Exception as e:
        print(f"Socket server error: {e}")

# Serve static files
def serve_static_files():
    try:
        static_dir_path = os.path.join(os.getcwd(), STATIC_DIR)
        os.chdir(static_dir_path)
        server_address = ('', HTTP_PORT)
        httpd = HTTPServer(server_address, HTTPHandler)
        print(f'Starting HTTP server on port {HTTP_PORT}')
        httpd.serve_forever()
    except Exception as e:
        print(f"HTTP server error: {e}")

# HTTP request handler for static files
class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path.strip('/')
            if os.path.exists(path):
                self.send_response(200)
                if path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                self.end_headers()
                with open(path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'Not Found')
        except Exception as e:
            print(f"Error handling static file request: {e}")

if __name__ == '__main__':
    # Start the socket server and HTTP server in separate threads
    socket_thread = Thread(target=socket_server)
    socket_thread.start()
    http_thread = Thread(target=serve_static_files)
    http_thread.start()