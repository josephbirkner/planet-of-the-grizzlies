# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Main_Menu(object):
    def setupUi(self, Main_Menu):
        Main_Menu.setObjectName("Main_Menu")
        Main_Menu.resize(214, 134)
        self.verticalLayout = QtWidgets.QVBoxLayout(Main_Menu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playButton = QtWidgets.QPushButton(Main_Menu)
        self.playButton.setObjectName("playButton")
        self.verticalLayout.addWidget(self.playButton)
        self.exitButton = QtWidgets.QPushButton(Main_Menu)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)

        self.retranslateUi(Main_Menu)
        QtCore.QMetaObject.connectSlotsByName(Main_Menu)

    def retranslateUi(self, Main_Menu):
        _translate = QtCore.QCoreApplication.translate
        Main_Menu.setWindowTitle(_translate("Main_Menu", "Dialog"))
        self.playButton.setText(_translate("Main_Menu", "Play"))
        self.exitButton.setText(_translate("Main_Menu", "Exit"))

