import socket

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
        s.bind((HOST, PORT))
except socket.error as msg:
        print('Bind failed. Error')
s.listen(3000)
while True:
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    a = conn.recv(4096)
    print(a)
     
s.close()
