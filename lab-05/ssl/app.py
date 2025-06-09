from flask import Flask, render_template, request
import socket, ssl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ssl_ui.html')

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection(('localhost', 12345)) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.sendall(message.encode())
                response = ssock.recv(1024).decode()
    except Exception as e:
        response = f"Lỗi kết nối SSL: {e}"

    return render_template('ssl_ui.html', result=response)

if __name__ == '__main__':
    app.run(debug=True)