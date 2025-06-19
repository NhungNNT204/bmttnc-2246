import socket

def handle_request(client_socket, request_data):
    first_line = request_data.split('\n')[0]
    try:
        method, path, _ = first_line.split()
    except ValueError:
        client_socket.close()
        return

    if path == "/admin":
        try:
            with open('admin.html', 'r', encoding='utf-8') as f:
                body = f.read()
        except FileNotFoundError:
            body = "<h1>Admin file not found</h1>"

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + body

    else:
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                body = f.read()
        except FileNotFoundError:
            body = "<h1>Index file not found</h1>"

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + body

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("🟢 Web Server đang lắng nghe tại cổng 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"🔗 Đã kết nối từ {client_address}")
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"📩 Yêu cầu nhận: {request_data}")
        handle_request(client_socket, request_data)

if __name__ == "__main__":
    main()
