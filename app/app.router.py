import http.server
import socketserver

# Define the HTTP request handler
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/message':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404)

# Define HTTP server parameters
host = 'localhost'
port = 3000

# Create and run the HTTP server
with socketserver.TCPServer((host, port), MyHttpRequestHandler) as httpd:
    print(f"HTTP server is running at http://{host}:{port}")
    httpd.serve_forever()
