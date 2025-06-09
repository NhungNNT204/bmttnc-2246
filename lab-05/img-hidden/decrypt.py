import sys
from PIL import Image

def decode_image(encoded_image_path):
    image = Image.open(encoded_image_path)
    width, height = image.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = image.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Giải mã nhị phân thành chuỗi ký tự cho đến khi gặp mã kết thúc
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111110':  # kết thúc nếu gặp dấu hiệu kết thúc (giống encrypt)
            break
        char = chr(int(byte, 2))
        message += char

    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("🕵️‍♀️ Decoded message:", decoded_message)

if __name__ == "__main__":
    main()