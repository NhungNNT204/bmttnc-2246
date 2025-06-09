import tornado.ioloop
import tornado.websocket
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        self.aes_key = None

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Reading...")
        tornado.websocket.websocket_connect(
            "ws://localhost:8888/websocket/",
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def maybe_retry_connection(self, future) -> None:
        try:
            self.connection = future.result()
        except:
            print("Could not reconnect, retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Disconnected, reconnecting...")
            self.connect_and_read()
            return
        if message.startswith("KEY:"):
            self.aes_key = base64.b64decode(message[4:])
            print("Received AES key from server.")
            self.send_message()
        elif message.startswith("CIPHERTEXT:"):
            ct = base64.b64decode(message[11:])
            iv = ct[:16]
            ciphertext = ct[16:]
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
            try:
                plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
                print(f"Decrypted from server: {plaintext}")
            except Exception as e:
                print(f"Error decrypting: {e}")
            self.send_message()
        elif message.startswith("ERROR:"):
            print(f"Lỗi từ server: {message[6:]}")
            self.send_message()
        else:
            print(f"Received: {message}")
        self.connection.read_message(callback=self.on_message)

    def send_message(self):
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg == "exit":
            self.stop()
            return
        self.connection.write_message(msg)

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()

if __name__ == "__main__":
    main()