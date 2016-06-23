# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potg_ingame.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_potg_ingame(object):
    def setupUi(self, potg_ingame):
        potg_ingame.setObjectName("potg_ingame")
        potg_ingame.resize(772, 551)
        self.gridLayout = QtWidgets.QGridLayout(potg_ingame)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(potg_ingame)
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 25)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.progressBar2 = QtWidgets.QProgressBar(potg_ingame)
        self.progressBar2.setProperty("value", 25)
        self.progressBar2.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar2.setObjectName("progressBar2")
        self.gridLayout.addWidget(self.progressBar2, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 3)
        self.lcdNumber = QtWidgets.QLCDNumber(potg_ingame)
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
        self.lcdNumber2 = QtWidgets.QLCDNumber(potg_ingame)
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.gridLayout.addWidget(self.lcdNumber2, 0, 2, 1, 1)

        self.retranslateUi(potg_ingame)
        QtCore.QMetaObject.connectSlotsByName(potg_ingame)

    def retranslateUi(self, potg_ingame):
        _translate = QtCore.QCoreApplication.translate
        potg_ingame.setWindowTitle(_translate("potg_ingame", "Form"))
        self.progressBar.setFormat(_translate("potg_ingame", "%p%"))

