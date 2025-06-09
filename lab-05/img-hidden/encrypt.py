import sys
from PIL import Image

def encode_image(image_path, message):
    image = Image.open(image_path)
    width, height = image.size

    # Chuyển message thành chuỗi nhị phân
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '11111110'  # 1 byte kết thúc thông điệp

    data_index = 0
    max_capacity = width * height * 3  # mỗi pixel có 3 kênh màu

    if len(binary_message) > max_capacity:
        print("❌ Lỗi: Ảnh không đủ dung lượng để chứa thông điệp.")
        return

    for row in range(height):
        for col in range(width):
            pixel = list(image.getpixel((col, row)))
            for channel in range(3):  # r, g, b
                if data_index < len(binary_message):
                    pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
            image.putpixel((col, row), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encode_image_path = 'encoded_image.png'
    image.save(encode_image_path)
    print("✅ Steganography complete. Encoded image saved as:", encode_image_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return
    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == "__main__":
    main()