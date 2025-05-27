def dao_nguc_chuoi(chuoi):
    return chuoi[::-1]  # Sử dụng hàm và in kết quả

input_string = input("Mời nhập chuỗi cần đảo ngược: ")
print("Chuỗi đảo ngược là:", dao_nguc_chuoi(input_string))