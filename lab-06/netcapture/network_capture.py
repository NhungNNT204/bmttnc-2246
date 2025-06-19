import subprocess
from scapy.all import sniff

def get_interfaces():
    result = subprocess.run(["powershell", "-Command", "Get-NetAdapter | Select-Object -ExpandProperty Name"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def packet_handler(packet):
    print(f"📦 {packet.summary()}")

interfaces = get_interfaces()
print("📶 Danh sách các giao diện mạng khả dụng:")
for i, iface in enumerate(interfaces, start=1):
    print(f"{i}. {iface}")

choice = int(input("🔧 Chọn giao diện để bắt gói tin (nhập số): "))
selected_iface = interfaces[choice - 1]
print(f"📡 Đang bắt gói tin trên giao diện: {selected_iface} ...")

sniff(iface=selected_iface, prn=packet_handler, filter="ip", store=False, promisc=True)
