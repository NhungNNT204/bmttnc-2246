from scapy.all import *

LOG_FILE = "icmp_log.txt"

def log_packet(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def modify_icmp_packet(packet):
    if packet.haslayer(ICMP):
        icmp = packet[ICMP]

        # Chỉ xử lý Echo Request (type=8)
        if icmp.type != 8:
            return

        original_info = f"""
[Original ICMP Packet]
Source IP: {packet[IP].src}
Destination IP: {packet[IP].dst}
Type: {icmp.type}
Code: {icmp.code}
ID: {icmp.id}
Sequence: {icmp.seq}
Load: {bytes(icmp.payload) if icmp.payload else b''}
"""
        print(original_info)
        log_packet(original_info.strip())

        # Tạo phản hồi ICMP
        new_load = b"This is a modified ICMP packet."
        response = IP(src=packet[IP].dst, dst=packet[IP].src) / ICMP(
            type=0,  # Echo Reply
            code=0,
            id=icmp.id,
            seq=icmp.seq
        ) / new_load

        modified_info = f"""
[Modified ICMP Reply]
Source IP: {response[IP].src}
Destination IP: {response[IP].dst}
Type: {response[ICMP].type}
Code: {response[ICMP].code}
ID: {response[ICMP].id}
Sequence: {response[ICMP].seq}
Load: {new_load}
{'=' * 40}
"""
        print(modified_info)
        log_packet(modified_info.strip())

        send(response, verbose=False)

def main():
    print("[INFO] Listening for ICMP Echo Requests... Press Ctrl+C to stop.")
    sniff(prn=modify_icmp_packet, filter="icmp", store=False)

if __name__ == "__main__":
    main()
