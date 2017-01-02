from registrationWindow import Ui_regWin
from clientWindow import Ui_clientWin 
from ChatBox import Ui_chatBox
#from CommWin import Ui_NetWindow
from PyQt5 import QtCore,QtWidgets
import socket
import funcs
import sys
import threading
import queue
sockLock = threading.Lock()
clientSock = ''
hostUserName =''
hostUserNo = ''
hostMacAdress = ''
HOST = '172.16.30.20'
PORT = funcs.PORT

class writingThread(QtCore.QThread):
	
	completeSignal = QtCore.pyqtSignal(str,str,str)

	def __init__(self,msg,q,key,parent = None):
		super(writingThread,self).__init__(parent)
		self.parent = parent
		self.key = key
		msg = msg.split(' ')
		self.fileName = msg[0]
		self.senderName = msg[1]
		self.q = q
		self.f = open(self.fileName,'wb')
		print("file "+msg[0]+ " from "+msg[1]+" opened in writing thread")

	def __del__(self):
		self.wait()
	
	def run(self):
		while True:
			data = self.q.get()
			if data == None:
				break
			self.f.write(data)
		self.f.close()
		print("File "+self.fileName+" from "+self.senderName+" completed")
		self.completeSignal.emit(self.key,self.fileName,self.senderName)
	

class readingThread(QtCore.QThread):

	sendingCompleteSignal = QtCore.pyqtSignal(str)

	def __init__(self,sock,uno,fno,rno,uname,fname,parent = None):
		super(readingThread,self).__init__(parent)
		self.parent = parent
		self.clientSock = sock
		self.roomNo = rno
		self.fileName = fname
		self.hostUserNo = uno
		self.fileNo = fno
		self.hostUserName = uname
		self.f = open(self.fileName,'rb')
		with sockLock:
			print("Sending - "+self.roomNo+self.fileName+" "+self.hostUserName)
			funcs.send_message(self.clientSock,self.hostUserNo,self.roomNo+self.fileName+" "+self.hostUserName,self.fileNo)	# sent first signal
		
	
	def __del__(self):
		self.wait()

	def run(self):
		room = self.roomNo.encode("utf-8")
		while True:
			rd = self.f.read(funcs.CHUNK_SIZE)
			data = room+rd
			data = funcs.create_packet(self.hostUserNo,self.fileNo,data)
			with sockLock:
				funcs.send_data(self.clientSock,data)
			if rd == b'':
				break
		self.f.close()
		print("File "+self.fileName+" sent")
		self.sendingCompleteSignal.emit(self.fileName)
		

class chatWin(QtWidgets.QWidget,Ui_chatBox):
	def __init__(self,message,name,uno,room,sock,parent = None):
		super(chatWin,self).__init__()
		self.setupUi(self,message)
		self.parent = parent
		self.hostUserName = name
		self.hostUserNo = uno
		self.clientSock = sock
		room = funcs.threeDigit(room)
		self.room = room
		self.fileNo = 1
		self.fileList = {}
		# connections
		self.userChat.returnPressed.connect(self.handleSend)
		self.listOnline.clicked.connect(self.handleOnline)
		self.exitButton.clicked.connect(self.handleClose)
		self.sendButton.clicked.connect(self.userChat.returnPressed)
		self.fileSendButton.clicked.connect(self.handleFileSend)		
	
	def handleClose(self):
		message = self.room + self.hostUserName+" left the room."
		try:
			with sockLock:
				funcs.send_message(self.clientSock,self.hostUserNo,message)
			self.close()
		except ConnectionError:
			self.chat.append("Server seems offline")

	def handleSend(self):	
		message = self.userChat.toPlainText()
		if not message:
			return
		self.userChat.clear()
		self.updateChat(self.hostUserName+" : "+message)
		message = self.room+self.hostUserName + " : " +message
		try:
			#print(message)
			with sockLock:
				print("Sending ",message)
				funcs.send_message(self.clientSock,self.hostUserNo,message)
		except ConnectionError:
			self.chat.append("Server seems offline")
	
	def updateChat(self,message):		
		self.chat.append(message)

	def handleOnline(self):
		self.parent.show()

	def writeFile(self,key,data):
		if not self.fileList.get(key):	#newFile
			msg = data.decode('utf-8')
			self.fileList[key] = queue.Queue()
			print("Newfile "+msg+" key "+key+" queue "+str(self.fileList[key]))
			th = writingThread(msg,self.fileList[key],key,self)
			th.completeSignal.connect(self.fileComplete)
			th.start()
		else:
			self.fileList[key].put(data)
		
	def fileComplete(self,key,fileName,senderName):
		print("File Complete")
		self.updateChat("File "+fileName+" recieved from "+senderName)
		del self.fileList[key]

	def handleFileSend(self):
		fileName = self.userChat.toPlainText()
		if not fileName:
			return
		print("Sending Filename = " + fileName)
		self.updateChat("Sending Filename " + fileName)
		msg = self.room+self.hostUserName+" is sending file "+fileName
		try:
			with sockLock:
				funcs.send_message(self.clientSock,self.hostUserNo,msg)
			th = readingThread(self.clientSock,self.hostUserNo,self.fileNo,self.room,self.hostUserName,fileName,self)
			th.sendingCompleteSignal.connect(self.sendingComplete)
			self.fileNo +=1		
			th.start()
		except ConnectionError:
			self.chat.append("Server seems offline")
	def sendingComplete(self,name):
		self.updateChat("File "+name+" sent")
		


class recievingThread(QtCore.QThread):

	updateListSignal = QtCore.pyqtSignal(str)
	newRoomSignal = QtCore.pyqtSignal(str,str)
	routeMessageSignal = QtCore.pyqtSignal(str,str)
	fileSignal = QtCore.pyqtSignal(str,str,bytes)
	def __init__(self,sock,parent = None):
		super(recievingThread,self).__init__()
		self.parent = parent
		self.clientSock =sock
	def __del__(self):
		self.wait()

	def run(self):	# Use Try except error handling
		while True:
			try:
				uno , fno , size = funcs.recieve_header(self.clientSock)
				if fno == 999:
					msg = funcs.recieve_message(self.clientSock,size)
					room = msg[0:3]
					msg = msg[3:len(msg)]
					print("Recieved ",msg)
					self.routeMessageSignal.emit(room,msg)	
				elif fno == 998: # new room creation
					msg = funcs.recieve_message(self.clientSock,size)
					msg = msg.split(' ',1)
					newroom = msg[0]
					msg = msg[1]
					self.newRoomSignal.emit(newroom,msg)
			
				elif fno == 997: # update list
					msg = funcs.recieve_message(self.clientSock,size)
					self.updateListSignal.emit(msg)
				elif fno <997:
					uno = str(uno)
					fno = str(fno)
					key = uno+fno
					data = funcs.recieve_data(self.clientSock,size)
					room = data[0:3].decode('utf-8')
					print("Recieved data for room "+room+" key = "+key)
					data = data[3:]
					self.fileSignal.emit(room,key,data)
			
			except ConnectionError:
				pass # to do error handling
				


class clWin(QtWidgets.QMainWindow,Ui_clientWin):	
	newFile = QtCore.pyqtSignal()
	
	def __init__(self,parent = None):
		super(clWin,self).__init__(parent)
		self.setupUi(self)
		self.rooms = {}
		self.show()
		self.clientSock = clientSock
		self.hostUserNo = hostUserNo
		self.hostUserName = hostUserName
		self.hostMacAdress = hostMacAdress
		# refresh timer to update list
		self.refreshTimer = QtCore.QTimer(self)
		self.refreshTimer.setInterval(10000)
		
	
		#connections
		self.refreshButton.clicked.connect(self.sendRefresh)
		self.roomButton.clicked.connect(self.makeRoom)
		self.exitButton.clicked.connect(self.close)
		self.refreshTimer.timeout.connect(self.sendRefresh)

	def makeRoom(self):
		users = ''
		items = self.onlineList.selectedItems()
		for item in items:
			users += item.text()+","
		users = users[0:len(users)-1]
		with sockLock:
			funcs.send_connect(self.clientSock,self.hostUserNo,users)
		
	def sendRefresh(self):
		with sockLock:
			funcs.send_message(self.clientSock,self.hostUserNo,'',997)
		
			
	def startRecieve(self):
		self.sendRefresh()
		self.refreshTimer.start()
		self.recvThread = recievingThread(self.clientSock,self)
		self.recvThread.updateListSignal.connect(self.refreshList)
		self.recvThread.newRoomSignal.connect(self.newRoom)
		self.recvThread.routeMessageSignal.connect(self.routeMessage)
		self.recvThread.fileSignal.connect(self.handleFile)
		self.recvThread.start()
	
	def refreshList(self,msg):
		self.onlineList.clear()
		msg = msg.split(" ")
		for user in msg:
			self.onlineList.addItem(user)
	def newRoom(self,roomNo,tittle):
		print("New Room "+roomNo)
		self.rooms[roomNo] = chatWin(tittle,self.hostUserName,self.hostUserNo,roomNo,self.clientSock,self)
		self.rooms[roomNo].show()
		self.hide()

	def routeMessage(self,roomNo,message):
		print("Routing ",message)
		self.rooms[roomNo].updateChat(message)

	def handleFile(self,roomNo,key,data):
		if data == b'':
			self.rooms[roomNo].writeFile(key,None)
		else:	
			self.rooms[roomNo].writeFile(key,data)
		


class RegWin(QtWidgets.QMainWindow,Ui_regWin):
	def __init__(self,parent = None):
		super(RegWin,self).__init__(parent)
		
		self.setupUi(self)
		self.connectionError = False
		# Connections
		self.exitButton.clicked.connect(self.close)
		self.userName.returnPressed.connect(self.connectButton.animateClick)
		self.connectButton.clicked.connect(self.handleConnect)
		self.show()
		try :
			global clientSock
			clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			clientSock.connect((HOST,PORT))
		except(ConnectionError):
			self.serverStatus.setText("Server Offline: Cannot Connect, press Exit to Exit")
			self.connectionError = True

	def handleConnect(self):
		if self.connectionError:
			return
		global hostUserName
		name = self.userName.text()
		self.userName.clear()
		if(name):
			print("UserNameEntered = ",name)
			try:
				funcs.send_message(clientSock,0,hostMacAdress+','+name)
				uno , fno , size = funcs.recieve_header(clientSock)
				reply = funcs.recieve_message(clientSock,size)
				self.serverStatus.setText(reply)
				print(reply)
				if reply[0] == 'C':
					uno , fno , size = funcs.recieve_header(clientSock)
					hostUserName = name
					hostUserNo = uno
					QtCore.QTimer.singleShot(200,self.close)

			except(ConnectionError):
				self.appName.setText("Cannot Connect, press Exit to Exit")
				self.connectionError = True
		else:
			self.serverStatus.setText("Enter a valid name")



if __name__ == "__main__":
	hostMacAdress = funcs.getmac()
	Regapp = QtWidgets.QApplication(sys.argv)
	window = RegWin()
	Regapp.exec_()
	if not hostUserName:
		exit()
	clapp = QtWidgets.QApplication(sys.argv)
	win = clWin()
	win.startRecieve()
	clapp.exec_()
	#print(hostUserName)
	print('Exiting')
	
	
	
