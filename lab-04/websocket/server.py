import random
import base64
import tornado.ioloop
import tornado.web
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()
    aes_key = get_random_bytes(16)  # Sinh key AES dùng chung

    def open(self):
        WebSocketServer.clients.add(self)
        # Gửi key AES cho client (base64)
        self.write_message("KEY:" + base64.b64encode(WebSocketServer.aes_key).decode())

    def on_close(self):
        WebSocketServer.clients.remove(self)

    def on_message(self, message):
        try:
            cipher = AES.new(WebSocketServer.aes_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
            result = base64.b64encode(cipher.iv + ct_bytes).decode()
            self.write_message("CIPHERTEXT:" + result)
        except Exception as e:
            self.write_message(f"ERROR: {str(e)}")
        # Không đóng kết nối, cho phép nhận tiếp message

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()

if __name__ == "__main__":
    main()