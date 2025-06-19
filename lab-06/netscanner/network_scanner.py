from scapy.all import ARP, Ether, srp
import socket

def get_local_subnet():
    # Tự động lấy địa chỉ IP của máy và đoán subnet
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = ".".join(local_ip.split(".")[:3]) + ".1/24"
        return subnet
    except Exception as e:
        print(f"⚠️ Không thể xác định subnet: {e}")
        return None

def scan_network(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

if __name__ == "__main__":
    subnet = get_local_subnet()
    if subnet:
        print("📡 Đang quét mạng LAN:", subnet)
        devices = scan_network(subnet)

        if devices:
            print("🕵️‍♂️ Các thiết bị tìm thấy trong mạng:")
            for device in devices:
                print(f"🔹 IP: {device['ip']} \t MAC: {device['mac']}")
        else:
            print("❌ Không phát hiện thiết bị nào.")
    else:
        print("❌ Không thể xác định subnet mạng.")
