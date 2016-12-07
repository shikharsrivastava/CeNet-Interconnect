import threading
import os
import socket
import funcs
import queue
HOST = funcs.HOST #'172.16.30.20'
PORT = funcs.PORT
write_lock = threading.Lock()
socket_lock = threading.Lock()
write_queues = {}


def print_help():
	print('''
	Commands -

	req - 					Request name of connected users

	connect [users] room [room number] -    Connected requested users to your broadcast room no
						Use - connect user1,user2,user3..usern room desired_room_no

	roomchat - 				Broadcast message to any of your rooms
						Use - roomchat desired_room_no hello world!

	roomsend -				Broadcast a file to any of your rooms
						use - roomsend desired_room_no file1,file2...file_n
	q -					Quit

	h -					Help		
		''')
room_lock = threading.Lock()
room_list = set()

def handle_recieve(sock):
	while True:
		try:
			uno , fno , size = funcs.recieve_header(sock)
			if fno == 999: # Message file to print
				msg = funcs.recieve_message(sock,size)
				print(msg)
			elif fno == 998:
				msg = funcs.recieve_message(sock,size)
				msg = msg.split(' ',1)
				newroom = msg[0]
				with room_lock:
					room_list.add(newroom)
				msg = msg[1]
				print("Connected to room " + newroom +" "+ msg)
			elif fno == 997:
				msg = funcs.recieve_message(sock,size)
				print(msg)
			elif fno < 997: # Other type of packets
				key = str(uno)+','+str(fno)
				if size == 0:
					handle_completion(key)
				else:
					data = funcs.recieve_data(sock,size)
					with write_lock:
						if write_queues.get(key,None):
							q = write_queues.get(key)
							q.put(data)
						else:
							msg = data.decode('utf-8')
							message = msg
							msg = msg.split(',') #filename,username
							file_name = msg[0]
							user_name = msg[1]
							print('Recieving File {} from {}'.format(file_name,user_name))
							q = queue.Queue()
							write_queues[key] = q
							write_thread = threading.Thread(target = write_file,args = [file_name,user_name,q],daemon = True)
							write_thread.start()	
			else:
				print('Unknown Data recieved')
		except(ConnectionError):
			print('Srever Disconnected')
			break

def handle_file_send(sock,file_num,uno,file_name,user_name,room):
	if len(room) < 3:
		room = '0'*(3-len(room))+room
	print("handling file {} num {} room {}".format(file_name,file_num,room))
	f = open(file_name,'rb')
	with socket_lock:
		funcs.send_message(sock,uno,room+file_name+','+user_name,file_num)
	room = room.encode('utf-8')
	data = f.read(funcs.CHUNK_SIZE)
	while data != b'':
		data = room + data
		data = funcs.create_packet(uno,file_num,data)
		with socket_lock:
			funcs.send_data(sock,data)
		data = f.read(funcs.CHUNK_SIZE)
	#Sending closing information
	data = room + data
	data = funcs.create_packet(uno,file_num,data)
	with socket_lock:
		funcs.send_data(sock,data)
	
	print('File {} transfered'.format(file_name))
	f.close()

def handle_completion(key):
	with write_lock:
		q = write_queues[key]
	if q:
		q.put(None)
		del write_queues[key]
	
def write_file(file_name,user_name,q):
	
	f = open(file_name,'wb')
	while True:
		data = q.get()
		if data == None:
			print('File {} from {} completed'.format(file_name,user_name)) 
			f.close()
			break
		f.write(data)
	
	
if __name__ == '__main__':
	print_help()
	try :
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((HOST,PORT))
		name , host_user_no = funcs.register_client(sock)
		file_no = 0
		recv_thread = threading.Thread(target = handle_recieve,args = [sock],daemon = True)
		recv_thread.start()
	except(ConnectionRefusedError,ConnectionError):
		print('The Server seems offline......\nPlease Try Again Later')
		exit()
	
	print('Connected to {} At {} '.format(HOST,PORT))

	while True:
		inp = input()
		try:
			inp = inp.split(' ',1)
			if 'h' == inp[0]:
				print_help()	
			elif 'q' == inp[0]:
				exit()			
			elif 'connect' == inp[0]:
				inp = inp[1]
				funcs.send_connect(sock,host_user_no,inp)
			elif 'roomchat' == inp[0]:
				inp = inp[1].split(' ',1) 			
				room = inp[0]
				with room_lock:
					if not room in room_list:
						print("Invalid room")
						continue
				message = name + ": " + inp[1]
				if len(room) <3:
					room = '0'*(3-len(room))+room
				message = room + message
				with socket_lock:
					funcs.send_message(sock,host_user_no,message)
			elif 'roomsend' == inp[0]:
				signal = inp[1].split(' ',1)
				room = signal[0]
				with room_lock:
					if not room in room_list:
						print("Invalid room")
						continue
				files = signal[1].split(',')
				for f in files:
					print('file {}'.format(f))
					file_no +=1
					send_thread = threading.Thread(target = handle_file_send,args=[sock,file_no,host_user_no,f,name,room],daemon = True)
					send_thread.start()
			elif 'req' == inp[0]:
				with socket_lock:
					funcs.send_message(sock,host_user_no,'',997)
			else:
				print('Wrong Message')
		except(ConnectionError):
			print('Server Disconnected')
			break
					
	
