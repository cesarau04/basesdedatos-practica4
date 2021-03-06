import socket 
import sys

#host = '192.168.0.107'
host = '10.43.62.206'
port = 4444
myself = 0
#my_data = ["","",""]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((host,port)) 
print("Connected!")

try:
	file = open("db.txt", "r")
	my_data = file.readline() #d→b→c
	if my_data == '':
		my_data = ["","",""]
	else:
		my_data = my_data.split('→')
except Exception:
	my_data = ["","",""]
	
	print("no such file")

data = s.recv(1024)
myself = data.decode()
myself = int(myself)
print("I'm node ", myself+1)

while True: 
	data = s.recv(1024) 
	data = data.decode()
	print("RECEIVED:  ", data)
	if data[:8] == "$<data>$":
		index = int(data[8:9])
		my_data[index] = data[9:]
	elif data == "$<smyov>$":
		msg = str(my_data[myself])
		s.send(msg.encode())
	elif data == "$<smybv>$":
		msg = str(my_data[(myself+1)%3])
		s.send(msg.encode())
	elif data == "$<status>$":
		msg = str(my_data)
		s.send(msg.encode())
	elif data == "":
		file = open("db.txt", "w")	
		ph = str(my_data[0]) + '→' + str(my_data[1]) +  '→' + str(my_data[2])
		file.write(ph)
		file.close()
		print("\n\nMy final variables:")
		print(my_data)
		s.close()
		sys.exit()

s.close() 
