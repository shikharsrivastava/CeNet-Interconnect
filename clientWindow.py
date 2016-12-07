
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_clientWin(object):
    def setupUi(self, clientWin):
        clientWin.setObjectName("clientWin")
        clientWin.resize(607, 597)
        self.centralwidget = QtWidgets.QWidget(clientWin)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout.addWidget(self.refreshButton, 2, 0, 1, 1)
        self.onlineList = QtWidgets.QListWidget(self.centralwidget)
        self.onlineList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.onlineList.setObjectName("onlineList")
        self.gridLayout.addWidget(self.onlineList, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.roomButton = QtWidgets.QPushButton(self.centralwidget)
        self.roomButton.setObjectName("roomButton")
        self.horizontalLayout.addWidget(self.roomButton)
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        clientWin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(clientWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 607, 19))
        self.menubar.setObjectName("menubar")
        clientWin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(clientWin)
        self.statusbar.setObjectName("statusbar")
        clientWin.setStatusBar(self.statusbar)

        self.retranslateUi(clientWin)
        QtCore.QMetaObject.connectSlotsByName(clientWin)

    def retranslateUi(self, clientWin):
        _translate = QtCore.QCoreApplication.translate
        clientWin.setWindowTitle(_translate("clientWin", "CeNet Client 2.0"))
        self.refreshButton.setText(_translate("clientWin", "Refresh"))
        self.roomButton.setText(_translate("clientWin", "Room"))
        self.exitButton.setText(_translate("clientWin", "Exit"))

