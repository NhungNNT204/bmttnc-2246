import socket

def handle_request(client_socket, request_data):
    # Tách dòng đầu tiên của HTTP request
    first_line = request_data.split('\n')[0]
    try:
        method, path, _ = first_line.split()
    except ValueError:
        client_socket.close()
        return

    # Xử lý dựa trên đường dẫn
    if path == "/admin":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Admin Page</h1>"
    elif path == "/":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Welcome to the Web Server</h1>"
    else:
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Page Not Found</h1>"

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
