from PyQt5 import QtWidgets
from rsa import Ui_MainWindow  # Giao diện được sinh ra từ rsa.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii


class RSAApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.public_key = None
        self.private_key = None

        # Kết nối nút với các chức năng
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt_message)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_message)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_verify.clicked.connect(self.verify_signature)

    def generate_keys(self):
        """Tạo cặp khóa RSA."""
        key_pair = RSA.generate(2048)
        self.private_key = key_pair
        self.public_key = key_pair.publickey()
        self.ui.txt_info.setPlainText("Keys generated successfully!")

    def encrypt_message(self):
        """Mã hóa thông điệp."""
        plaintext = self.ui.txt_plain_text.toPlainText()
        if not self.public_key:
            self.ui.txt_info.setPlainText("Error: Public key not generated!")
            return

        cipher = PKCS1_OAEP.new(self.public_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        self.ui.txt_cipher_text.setPlainText(binascii.hexlify(ciphertext).decode())

    def decrypt_message(self):
        """Giải mã thông điệp."""
        ciphertext = self.ui.txt_cipher_text.toPlainText()
        if not self.private_key:
            self.ui.txt_info.setPlainText("Error: Private key not generated!")
            return

        cipher = PKCS1_OAEP.new(self.private_key)
        plaintext = cipher.decrypt(binascii.unhexlify(ciphertext.encode()))
        self.ui.txt_plain_text.setPlainText(plaintext.decode())

    def sign_message(self):
        """Ký thông điệp."""
        plaintext = self.ui.txt_plain_text.toPlainText()
        if not self.private_key:
            self.ui.txt_info.setPlainText("Error: Private key not generated!")
            return

        hash_value = SHA256.new(plaintext.encode())
        signature = pkcs1_15.new(self.private_key).sign(hash_value)
        self.ui.txt_sign.setPlainText(binascii.hexlify(signature).decode())

    def verify_signature(self):
        """Xác minh chữ ký."""
        plaintext = self.ui.txt_plain_text.toPlainText()
        signature = self.ui.txt_sign.toPlainText()
        if not self.public_key:
            self.ui.txt_info.setPlainText("Error: Public key not generated!")
            return

        hash_value = SHA256.new(plaintext.encode())
        try:
            pkcs1_15.new(self.public_key).verify(hash_value, binascii.unhexlify(signature.encode()))
            self.ui.txt_info.setPlainText("Signature verified successfully!")
        except (ValueError, TypeError):
            self.ui.txt_info.setPlainText("Signature verification failed!")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RSAApp()
    window.show()
    sys.exit(app.exec_())
