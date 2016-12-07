import socket
from uuid import getnode as get_mac
import threading

HOST = socket.gethostname()
PORT = 8889
CHUNK_SIZE = 900
HEADER_SIZE = 11 #3 digit user no , 3 digit file_no , 3 digit data_size
# fno also acts as signal
# 999 simple message
# 998 connection request
# 997 request connected users
# 000 is uno for server
# 000,000,000 represent name registration error
# size 000 represents the end of the file

def send_data(sock,data):
	sock.sendall(data)
def threeDigit(s):
	if(len(s)<3):
		s = '0'*(3-len(s))+s
	return s

def create_header(uno,fno,size):
	uno = str(uno)
	if len(uno) < 3:
		uno = '0'*(3-len(uno)) + uno
	fno = str(fno)
	if len(fno) < 3:
		fno = '0'*(3-len(fno)) + fno
	size = str(size)
	if len(size) < 3:
		size = '0'*(3-len(size)) + size
	header = uno+','+fno+','+size
	header = header.encode('utf-8')
	return header

def create_listening_socket(host,port,size):
	listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listening_socket.bind((host,port))
	listening_socket.listen(100)
	return listening_socket

def recieve_data(sock,size = 4096):
	data = bytes()
	while size:
		recv = sock.recv(size)
		if not recv:
			raise ConnectionError()
		data += recv
		size -= len(recv)
	return data

def recieve_header(sock):
	data = recieve_data(sock,HEADER_SIZE)
	data =  data.decode('utf-8')
	data = data.split(',')
	return int(data[0]) , int(data[1]) , int (data[2])

def recieve_message(sock,size):
	msg = recieve_data(sock,size)
	msg = msg.decode('utf-8')
	return msg

def create_packet(uno,fno,data):
	header = create_header(uno,fno,len(data))
	data = header + data
	return data

def send_connect(sock,uno,message):
	send_message(sock,uno,message,998)

def send_message(sock,uno,message,sig = 999):
	message = message.encode('utf-8')
	header = create_header(uno,sig,len(message))
	message = header+message
	send_data(sock,message)

def register_client(sock):
	mac_address = getmac()
	while True:
		name = input('Enter username : ')
		send_message(sock,0,mac_address+','+name)
		uno , fno , size = recieve_header(sock)
		reply = recieve_message(sock,size)
		print(reply)
		if reply[0] == 'C':
			break

	uno , fno , size = recieve_header(sock)
	print('User Number assigned = {}'.format(uno))
	return name , uno

def getmac():
	mac = get_mac()
	mac = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
	return mac
