# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potg_characterselect.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(655, 541)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.select_button = QtWidgets.QPushButton(Form)
        self.select_button.setObjectName("select_button")
        self.gridLayout.addWidget(self.select_button, 3, 2, 1, 1)
        self.player_1_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_1_button.sizePolicy().hasHeightForWidth())
        self.player_1_button.setSizePolicy(sizePolicy)
        self.player_1_button.setMinimumSize(QtCore.QSize(200, 200))
        self.player_1_button.setText("")
        self.player_1_button.setObjectName("player_1_button")
        self.gridLayout.addWidget(self.player_1_button, 2, 1, 1, 1)
        self.player_2_button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_2_button.sizePolicy().hasHeightForWidth())
        self.player_2_button.setSizePolicy(sizePolicy)
        self.player_2_button.setMinimumSize(QtCore.QSize(200, 200))
        self.player_2_button.setText("")
        self.player_2_button.setObjectName("player_2_button")
        self.gridLayout.addWidget(self.player_2_button, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 2)
        self.cancel_button = QtWidgets.QPushButton(Form)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.select_button.setText(_translate("Form", "Select"))
        self.label.setText(_translate("Form", "Choose your appearance!"))
        self.cancel_button.setText(_translate("Form", "Cancel"))

