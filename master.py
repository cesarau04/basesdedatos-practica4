import socket 
from threading import Thread
#from numpy import array_split

class Nodo():
	def __init__(self, sock:socket, chunck):
		self.sock = sock
		self.chunck = chunck
		self.neighbour_chunk = (chunck+1)%3
		self.sock.send(str(chunck).encode())
	
	def send_data(self):
		msg =  ("$<data>$" + str(self.chunck) + str(splited_message[self.chunck]))
		self.sock.send(msg.encode())
		return 
	
	def send_backup(self):
		msg =  ("$<data>$" + str(self.neighbour_chunk) + str(splited_message[self.neighbour_chunk]))
		self.sock.send(msg.encode())
		return 

	def read_data(self):
		msg = "$<smyov>$" #send me your original value
		self.sock.send(msg.encode())
		data = self.sock.recv(1024)
		return data.decode()

	def read_backup(self):
		msg = "$<smybv>$" #send me your backup value
		self.sock.send(msg.encode())
		data = self.sock.recv(1024)
		return data.decode()

	def status(self):
		msg = "$<status>$"
		self.sock.send(msg.encode())
		data = self.sock.recv(1024)
		return data.decode()
	
	def close(self):
		return self.sock.close()

def fragmenter(file):
    ans=[]
    size=int(len(file)/3)
    residuo=len(file)%3
    inc=0
    ant=0
    for i in range(3):
        ant=inc
        if(residuo!=0):
            inc+=1
            residuo-=1
        ans.append(file[size*i+ant:size*(i+1)+inc])       
    return ans

#host = "192.168.0.107"
host = "10.43.62.206"
port = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host, port)) 
print("BINDED at:", host, " ", port) 
s.listen(3) 
print("Waiting for 3 slaves...\n") 
_ = []
for i in range(3): 
	c, addr = s.accept() 
	print("Slave#",i+1," connected in:", addr[0], ":", addr[1]) 
	_.append((c,i))

node1 = Nodo(_[0][0],_[0][1])
node2 = Nodo(_[1][0],_[1][1])
node3 = Nodo(_[2][0],_[2][1])
del _

while(True):
	option = input(">")
	if node1.status() == '':
		node1.close()
	if node2.status() == '':
		node2.close()
	if node3.status() == '':
		node3.close()
	if option == 'set msg':
		splited_message = input(">>>")
		splited_message = fragmenter(splited_message)
	elif option == 'save':
		err = 0
		try:
			node1.send_data()
			node1.send_backup()
			node2.send_data()
			node2.send_backup()
			node3.send_data()
			node3.send_backup()
			if err == 0:
				print("Data saved successfully")
		except Exception:
			err = 1
			print(">>Error, couldn't save info into system")
	elif option == 'read':
		error = -1
		try:
			info1 = node1.read_data()
			if info1 == '':
				print("node1: No hay datos")
		except Exception:
			error = 1
			print("Error while reading node 1")
		try:
			info2 = node2.read_data()
			if info2 == '':
				print("node2: No hay datos")
		except Exception:
			error = 2
			print("Error while reading node 2")
		try:
			info3 = node3.read_data()
			if info3 == '':
				print("node3: No hay datos")
		except Exception:
			error = 3
			print("Error while reading node 3")
		
		if error != -1:
			if error == 1:
				info1= node3.read_backup()
			elif error == 2:
				info2 = node1.read_backup()
			elif error == 3:
				info3 = node2.read_backup()

		print("node1: " + str(info1) + "\tnode2: " + str(info2) + "\tnode3: " + str(info3))
	elif option == 'exit':
		node1.close()
		node2.close()
		node3.close()
		s.close()
		print("....................................")
		break
