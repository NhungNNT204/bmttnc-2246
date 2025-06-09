import hashlib

def calculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))  # Chuyển đổi chuỗi thành bytes và cập nhật vào hash
    return sha256_hash.hexdigest()  # Trả về chuỗi hex của hash

data_to_hash = input("Nhập chuỗi để hash bằng SHA-256: ")
hash_value = calculate_sha256_hash(data_to_hash)
print("Giá trị hash SHA-256:", hash_value)