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
        MainMenu.resize(824, 584)
        self.gridLayout = QtWidgets.QGridLayout(MainMenu)
        self.gridLayout.setObjectName("gridLayout")
        self.exitButton = QtWidgets.QPushButton(MainMenu)
        self.exitButton.setObjectName("exitButton")
        self.gridLayout.addWidget(self.exitButton, 3, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(MainMenu)
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 25)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.playButton = QtWidgets.QPushButton(MainMenu)
        self.playButton.setObjectName("playButton")
        self.gridLayout.addWidget(self.playButton, 3, 0, 1, 1)
        self.progressBar2 = QtWidgets.QProgressBar(MainMenu)
        self.progressBar2.setProperty("value", 25)
        self.progressBar2.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar2.setObjectName("progressBar2")
        self.gridLayout.addWidget(self.progressBar2, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.lcdNumber = QtWidgets.QLCDNumber(MainMenu)
        self.lcdNumber.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lcdNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumber.setAutoFillBackground(False)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(5)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout.addWidget(self.lcdNumber, 0, 0, 1, 1)
        self.lcdNumber2 = QtWidgets.QLCDNumber(MainMenu)
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.gridLayout.addWidget(self.lcdNumber2, 0, 1, 1, 1)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Form"))
        self.exitButton.setText(_translate("MainMenu", "Exit"))
        self.progressBar.setFormat(_translate("MainMenu", "%p%"))
        self.playButton.setToolTip(_translate("MainMenu", "<html><head/><body><p><br/></p></body></html>"))
        self.playButton.setText(_translate("MainMenu", "Play"))

