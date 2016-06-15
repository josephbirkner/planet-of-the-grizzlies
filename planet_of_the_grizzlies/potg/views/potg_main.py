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
        MainMenu.resize(897, 586)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainMenu)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(MainMenu)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.playButton = QtWidgets.QPushButton(MainMenu)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout.addWidget(self.playButton)
        self.exitButton = QtWidgets.QPushButton(MainMenu)
        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.progressBar2 = QtWidgets.QProgressBar(MainMenu)
        self.progressBar2.setProperty("value", 24)
        self.progressBar2.setObjectName("progressBar2")
        self.horizontalLayout.addWidget(self.progressBar2)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Form"))
        self.playButton.setText(_translate("MainMenu", "Play"))
        self.exitButton.setText(_translate("MainMenu", "Exit"))

