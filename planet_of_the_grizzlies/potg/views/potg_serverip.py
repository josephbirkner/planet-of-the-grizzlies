# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potg_serverip.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_potg_serverip(object):
    def setupUi(self, potg_serverip):
        potg_serverip.setObjectName("potg_serverip")
        potg_serverip.resize(665, 585)
        self.gridLayout = QtWidgets.QGridLayout(potg_serverip)
        self.gridLayout.setObjectName("gridLayout")
        self.connect_button = QtWidgets.QPushButton(potg_serverip)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy)
        self.connect_button.setMinimumSize(QtCore.QSize(100, 0))
        self.connect_button.setObjectName("connect_button")
        self.gridLayout.addWidget(self.connect_button, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(potg_serverip)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QtCore.QSize(100, 0))
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(potg_serverip)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(potg_serverip)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 4)

        self.retranslateUi(potg_serverip)
        QtCore.QMetaObject.connectSlotsByName(potg_serverip)

    def retranslateUi(self, potg_serverip):
        _translate = QtCore.QCoreApplication.translate
        potg_serverip.setWindowTitle(_translate("potg_serverip", "Form"))
        self.connect_button.setText(_translate("potg_serverip", "Connect"))
        self.cancel_button.setText(_translate("potg_serverip", "Cancel"))
        self.label.setText(_translate("potg_serverip", "Please enter the servers IP Address:"))
        self.lineEdit.setInputMask(_translate("potg_serverip", "000.000.000.000;_"))
        self.lineEdit.setText(_translate("potg_serverip", "127.0.0.1"))

