# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'registrationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_regWin(object):
    def setupUi(self, regWin):
        regWin.setObjectName("regWin")
        regWin.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(regWin)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.appName = QtWidgets.QLabel(self.centralwidget)
        self.appName.setAlignment(QtCore.Qt.AlignCenter)
        self.appName.setObjectName("appName")
        self.gridLayout.addWidget(self.appName, 1, 0, 1, 1)
        self.serverStatus = QtWidgets.QLabel(self.centralwidget)
        self.serverStatus.setText("")
        self.serverStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.serverStatus.setObjectName("serverStatus")
        self.gridLayout.addWidget(self.serverStatus, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameLabel.setObjectName("usernameLabel")
        self.horizontalLayout.addWidget(self.usernameLabel)
        self.userName = QtWidgets.QLineEdit(self.centralwidget)
        self.userName.setPlaceholderText("")
        self.userName.setObjectName("userName")
        self.horizontalLayout.addWidget(self.userName)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)
        self.gridLayout_3.addLayout(self.verticalLayout, 2, 0, 1, 1)
        regWin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(regWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        regWin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(regWin)
        self.statusbar.setObjectName("statusbar")
        regWin.setStatusBar(self.statusbar)

        self.retranslateUi(regWin)
        QtCore.QMetaObject.connectSlotsByName(regWin)

    def retranslateUi(self, regWin):
        _translate = QtCore.QCoreApplication.translate
        regWin.setWindowTitle(_translate("regWin", "CeNet 2.0 Registration"))
        self.appName.setText(_translate("regWin", "CeNet 2.0"))
        self.usernameLabel.setText(_translate("regWin", "Enter UserName"))
        self.connectButton.setText(_translate("regWin", "Connect "))
        self.exitButton.setText(_translate("regWin", "Exit :("))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    regWin = QtWidgets.QMainWindow()
    ui = Ui_regWin()
    ui.setupUi(regWin)
    regWin.show()
    sys.exit(app.exec_())

