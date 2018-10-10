import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
sock.connect(("10.43.34.159", 8888))
#sock.connect(("localhost", 8888))

while True:
    sock.send(b"Hola amiguito")