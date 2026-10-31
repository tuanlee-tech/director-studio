import socket

for port in [9222, 9223, 9224, 9225, 9226, 9227]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    r = s.connect_ex(("127.0.0.1", port))
    s.close()
    print(f"Port {port}: {'OPEN' if r == 0 else 'CLOSED'}")
