import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]

def scan_ports_socket(target, timeout=2):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((target, port)) == 0:
                    open_ports.append(port)
        except socket.error:
            continue
    return open_ports

def main():
    domain = input("Enter the target domain or IP: ")
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        print("Could not resolve domain.")
        return
    ports = scan_ports_socket(ip)
    if ports:
        print("Open ports:", ports)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
