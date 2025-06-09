from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    file = request.files['image']
    message = request.form['message']
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
    file.save(path)

    img = Image.open(path)
    binary = ''.join(format(ord(i), '08b') for i in message) + '11111110'

    data_index = 0
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if data_index < len(binary):
                r = (r & ~1) | int(binary[data_index])
                data_index += 1
            if data_index < len(binary):
                g = (g & ~1) | int(binary[data_index])
                data_index += 1
            if data_index < len(binary):
                b = (b & ~1) | int(binary[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
            if data_index >= len(binary):
                break
        if data_index >= len(binary):
            break

    encoded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_image.png')
    img.save(encoded_path)
    return f'✅ Đã ẩn thông điệp. <a href="/{encoded_path}" target="_blank">Xem ảnh</a>'

@app.route('/decode', methods=['POST'])
def decode():
    file = request.files['image']
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'decode_input.png')
    file.save(path)

    img = Image.open(path)
    binary = ""
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary += bin(r)[-1]
            binary += bin(g)[-1]
            binary += bin(b)[-1]

    message = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte == '11111110':
            break
        message += chr(int(byte, 2))

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)