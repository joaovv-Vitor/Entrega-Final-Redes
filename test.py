import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", 5001))  # Porta do broadcast

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Recebi: {data} de {addr}")
    sock.sendto(b"DISCOVERY_RESPONSE", addr)
