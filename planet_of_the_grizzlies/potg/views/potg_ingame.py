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
        self.health_bar = QtWidgets.QProgressBar(potg_ingame)
        self.health_bar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.health_bar.setAutoFillBackground(False)
        self.health_bar.setProperty("value", 100)
        self.health_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.health_bar.setTextVisible(True)
        self.health_bar.setInvertedAppearance(True)
        self.health_bar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.health_bar.setObjectName("health_bar")
        self.gridLayout.addWidget(self.health_bar, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        self.retranslateUi(potg_ingame)
        QtCore.QMetaObject.connectSlotsByName(potg_ingame)

    def retranslateUi(self, potg_ingame):
        _translate = QtCore.QCoreApplication.translate
        potg_ingame.setWindowTitle(_translate("potg_ingame", "Form"))
        self.health_bar.setFormat(_translate("potg_ingame", "%p%"))

