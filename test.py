

from PyQt5 import QtCore, QtGui, QtWidgets

# New widget wchich overrides QTextEdit's return pressed event

class chatText(QtWidgets.QTextEdit):
	returnPressed = QtCore.pyqtSignal()
	def __init__(self, parent):
		super (chatText, self).__init__(parent)

	def keyPressEvent(self, qKeyEvent):
		if qKeyEvent.key() == QtCore.Qt.Key_Return and qKeyEvent.modifiers() != QtCore.Qt.ShiftModifier: 
			self.returnPressed.emit()
		else:
			super().keyPressEvent(qKeyEvent)

class Ui_chatBox(object):
    def setupUi(self, chatBox,message):
        chatBox.setObjectName("chatBox")
        chatBox.resize(473, 294)
        self.gridLayout = QtWidgets.QGridLayout(chatBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.chatLabel = QtWidgets.QLabel(chatBox)
        self.chatLabel.setObjectName("chatLabel")
        self.verticalLayout.addWidget(self.chatLabel)
        self.userChat = QtWidgets.QTextEdit(chatBox)
        self.userChat.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.userChat.setObjectName("userChat")
        self.verticalLayout.addWidget(self.userChat)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 4, 1)
        self.chat = QtWidgets.QTextEdit(chatBox)
        self.chat.setEnabled(True)
        self.chat.setReadOnly(True)
        self.chat.setObjectName("chat")
        self.gridLayout.addWidget(self.chat, 0, 0, 1, 2)
        self.listOnline = QtWidgets.QPushButton(chatBox)
        self.listOnline.setObjectName("listOnline")
        self.gridLayout.addWidget(self.listOnline, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(chatBox)
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 3, 1, 1, 1)
        self.exitButton = QtWidgets.QPushButton(chatBox)
        self.exitButton.setObjectName("exitButton")
        self.gridLayout.addWidget(self.exitButton, 4, 1, 1, 1)
        self.fileSendButton = QtWidgets.QPushButton(chatBox)
        self.fileSendButton.setObjectName("fileSendButton")
        self.gridLayout.addWidget(self.fileSendButton, 2, 1, 1, 1)

        self.retranslateUi(chatBox,message)
        self.exitButton.clicked.connect(chatBox.close)
        self.sendButton.clicked.connect(self.userChat.clear)
        self.fileSendButton.clicked.connect(self.userChat.clear)
        QtCore.QMetaObject.connectSlotsByName(chatBox)

    def retranslateUi(self, chatBox,message):
        _translate = QtCore.QCoreApplication.translate
        chatBox.setWindowTitle(_translate("chatBox", message))
        self.chatLabel.setText(_translate("chatBox", "Enter Message"))
        self.listOnline.setText(_translate("chatBox", "Online"))
        self.sendButton.setText(_translate("chatBox", "Send"))
        self.exitButton.setText(_translate("chatBox", "Exit"))
        self.fileSendButton.setText(_translate("chatBox", "FileSend"))



