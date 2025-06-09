import sys
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import tornado.ioloop
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class WebSocketClientThread(QThread):
    received = pyqtSignal(str)
    decrypted = pyqtSignal(str)
    error = pyqtSignal(str)
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    key_received = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.aes_key = None
        self.connection = None
        self.io_loop = tornado.ioloop.IOLoop()
        self.running = True
        self.msg_to_send = None

    def run(self):
        self.io_loop.add_callback(self.connect_and_read)
        self.io_loop.start()

    def connect_and_read(self):
        tornado.websocket.websocket_connect(
            self.url,
            callback=self.on_connect,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def on_connect(self, future):
        try:
            self.connection = future.result()
            self.connected.emit()
        except Exception as e:
            self.error.emit(f"Could not connect: {e}")
            self.io_loop.stop()

    def on_message(self, message):
        if message is None:
            self.disconnected.emit()
            self.io_loop.stop()
            return
        if message.startswith("KEY:"):
            self.aes_key = base64.b64decode(message[4:])
            self.key_received.emit(message[4:])
        elif message.startswith("CIPHERTEXT:"):
            ct = base64.b64decode(message[11:])
            iv = ct[:16]
            ciphertext = ct[16:]
            try:
                cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
                plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
                self.decrypted.emit(plaintext)
            except Exception as e:
                self.error.emit(f"Error decrypting: {e}")
            self.received.emit(message[11:])
        elif message.startswith("ERROR:"):
            self.error.emit(message[6:])
        else:
            self.received.emit(message)
        if self.connection:
            self.connection.read_message(callback=self.on_message)

    def send_message(self, msg):
        if self.connection:
            self.connection.write_message(msg)

class WebSocketClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebSocket AES Client UI')
        self.setGeometry(300, 300, 500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText('Nhập thông điệp gửi tới server...')
        self.send_btn = QPushButton('Gửi')
        self.status = QLabel('Trạng thái: Chưa kết nối')
        self.key_label = QLabel('AES Key: (chưa nhận)')
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.key_label)
        self.layout.addWidget(QLabel('Log:'))
        self.layout.addWidget(self.log)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.send_btn)
        self.send_btn.clicked.connect(self.send_message)
        self.client_thread = WebSocketClientThread('ws://localhost:8888/websocket/')
        self.client_thread.received.connect(self.on_received)
        self.client_thread.decrypted.connect(self.on_decrypted)
        self.client_thread.error.connect(self.on_error)
        self.client_thread.connected.connect(self.on_connected)
        self.client_thread.disconnected.connect(self.on_disconnected)
        self.client_thread.key_received.connect(self.on_key_received)
        self.client_thread.start()

    def on_connected(self):
        self.status.setText('Trạng thái: Đã kết nối')
        self.log.append('Đã kết nối tới server.')

    def on_disconnected(self):
        self.status.setText('Trạng thái: Đã ngắt kết nối')
        self.log.append('Đã ngắt kết nối với server.')

    def on_key_received(self, key):
        self.key_label.setText(f'AES Key: {key}')
        self.log.append(f'Nhận AES key từ server: {key}')

    def on_received(self, ciphertext):
        self.log.append(f'Ciphertext (base64): {ciphertext}')

    def on_decrypted(self, plaintext):
        self.log.append(f'Giải mã: {plaintext}')

    def on_error(self, err):
        self.log.append(f'Lỗi: {err}')
        QMessageBox.warning(self, 'Lỗi', err)

    def send_message(self):
        msg = self.input.text()
        if not msg:
            return
        self.log.append(f'Gửi: {msg}')
        self.client_thread.send_message(msg)
        self.input.clear()

    def closeEvent(self, event):
        self.client_thread.io_loop.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebSocketClientUI()
    window.show()
    sys.exit(app.exec_())
