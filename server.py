import threading
import funcs
import queue
appname = 'CeNet'
version = '2.0'
HOST = '127.0.0.1' #funcs.HOST
PORT = funcs.PORT
MAX_ROOMS = 100
send_queues_lock = threading.Lock()
connected_lock = threading.Lock()
room_no_lock = threading.Lock()
room_lock = threading.Lock()
address_to_name_lock = threading.Lock() 
user_no_lock = threading.Lock()
room_no = 0
connected = {}
room_list = {} 
send_queues = {}
address_to_name = {}
user_no = 0 


def RegisterClient(sock,client_user_no,q):
	client_key = None
	try:
		retry = True
		while retry:
			uno, fno, size = funcs.recieve_header(sock)
			if fno == 999:
				mac_client, client_name = funcs.recieve_message(sock, size).split(',')
				with connected_lock:
					if connected.get(client_name, None):
						print('Client {} already present'.format(client_name))
					else:
						print('Client {}@{} registered'.format(mac_client, client_name))
						retry = False
				if retry:
					funcs.send_message(sock, 0, 'Server: Client named {} already present'.format(client_name))
				else:
					funcs.send_message(sock, 0, 'Connected to ' + appname + ' ' + version)
			else:
				print('Client name not recieved')
		print('Client {} : {} user_number = {}'.format(client_name, mac_client, client_user_no))
		client_key = mac_client + '@' + str(client_user_no)
		with send_queues_lock:
			send_queues[client_key] = q
		with address_to_name_lock:
			address_to_name[client_key] = client_name
		with connected_lock:
			connected[client_name] = client_key
		# sending user number
		funcs.send_message(sock, client_user_no, '')

		sending_thread = threading.Thread(target=handle_client_send, args=[sock, client_key, q], daemon=True)
		sending_thread.start()
		return client_name,mac_client,client_key

	except (EOFError, ConnectionError):
		handle_disconnect(sock, client_key)
		return None,None,None


def handle_disconnect(sock, key):
	print('Disconnecting {}'.format(key))
	with address_to_name_lock:
		name = address_to_name.get(key, None)
	if name == None:
		sock.close()
	else:

		del address_to_name[key]
		del connected[name]
		with room_lock:
			for room in room_list.keys():
				if key in room_list[room]:
					room_list[room].remove(key)
		with send_queues_lock:
			q = send_queues.get(key, None)
		if q:
			q.put(None)
			del send_queues[key]
			print('{} Disconnectd : {}'.format(name, key))
			sock.close()


def handle_client_recieve(sock,client_user_no,q):
	'''recieve names and other information'''
	global room_no
	#client registration
	client_name,mac_client,client_key=RegisterClient(sock,client_user_no, q)
	if not client_key:
		return

	''' Client Registration on server complete'''

	#starting of reception
	while True:
		try:
			uno,fno,size = funcs.recieve_header(sock)
			if fno == 998:	#Connect signal
				users = funcs.recieve_message(sock,size)
				users +=  ','+client_name
				with room_no_lock:
					room = room_no+1
					room_no += 1
				room = funcs.threeDigit(str(room))
				data = (room + " " + users + " by "+client_name).encode('utf-8')
				packet = funcs.create_packet(0,998,data)
				print('Connection request from {}:{}'.format(client_name,client_name+'@'+mac_client))
				print('Users Requested -> {}'.format(users))
				users = users.split(',') #user list 
				
				with room_lock:
						room_list[room] = set()

				for user in users:
					with connected_lock:
						ck = connected.get(user)
					if ck:
						send_to(ck,packet)
					with room_lock:
						room_list[room].add(ck)						
			
			elif fno == 997: # connected user request
				print("{} requested Connected users".format(client_name))
				message = bytes()
				with connected_lock:
					for user in connected.keys():
						message += (user+" ").encode('utf-8')
				message = message[0:len(message)-1]
				message_packet = funcs.create_packet(0,997,message) # 000 is uno for server,  message from 000 is message from server
				send_to(client_key,message_packet)
			else : #Chat message
				data = funcs.recieve_data(sock,size)
				room = data[0:3].decode('utf-8')
				print('Recieved packet for room {}'.format(room))
				data_packet = funcs.create_packet(uno,fno,data)
				with room_lock:
					for ck in room_list[room]:
						if client_key != ck:
							send_to(ck,data_packet)
											
					
		
		except (EOFError,ConnectionError):
			handle_disconnect(sock,client_key)
			break
		
def send_to(key,data):
	with send_queues_lock:
		if send_queues.get(key,None):
			send_queues[key].put(data)
			return True
		else:
			print('User {} not present'.format(key))
			return False	

def handle_client_send(sock,key,q):
	''' Handles data to be sent to the client '''
	while True:
		data = q.get()
		if data == None: break
		try:
			funcs.send_data(sock,data)
			print('Sent data for {}'.format(key))
		except (ConnectionError , BrokenPipeError):
			handle_disconnect(sock,key)



if __name__ == '__main__':
	print(appname + ' Server')
	print("Host : {}".format(funcs.HOST))
	listening_socket = funcs.create_listening_socket(HOST,PORT,100)
	listening_address = listening_socket.getsockname()
	print('Listening on {}'.format(listening_address))
	i = 0
	while True:
		client_socket,client_address = listening_socket.accept()
		q = queue.Queue()
		print('New conenction from : {}'.format(client_address))
		with user_no_lock:
			user_no += 1
			th = threading.Thread(target = handle_client_recieve,args = [client_socket,user_no,q],daemon = True)
		th.start()
		
		
