# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potg_main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(170, 98)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainMenu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.playButton = QtWidgets.QPushButton(MainMenu)
        self.playButton.setObjectName("playButton")
        self.verticalLayout.addWidget(self.playButton)
        self.exitButton = QtWidgets.QPushButton(MainMenu)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Form"))
        self.playButton.setText(_translate("MainMenu", "Play"))
        self.exitButton.setText(_translate("MainMenu", "Exit"))

