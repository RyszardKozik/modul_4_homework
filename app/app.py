from flask import Flask, render_template, request, redirect, url_for
import json
import socket

app = Flask(__name__, template_folder='templates')

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    message = request.form['message']
    data = {'username': username, 'message': message}
    send_to_socket(data)
    return redirect(url_for('index'))

def send_to_socket(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode('utf-8'), (SOCKET_HOST, SOCKET_PORT))

if __name__ == '__main__':
    app.run(debug=True)