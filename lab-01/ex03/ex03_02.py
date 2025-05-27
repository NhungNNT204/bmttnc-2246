def dao_nguc_list(lst):
    return lst[::-1]

# Nhập danh sách từ người dùng và xử lý chuỗi
input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))

# Sử dụng hàm và in kết quả
list_dao_nguc = dao_nguc_list(numbers)
print("List sau khi đảo ngược:", list_dao_nguc)