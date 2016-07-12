# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potg_main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_potg_main(object):
    def setupUi(self, potg_main):
        potg_main.setObjectName("potg_main")
        potg_main.resize(327, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(potg_main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.create_server_button = QtWidgets.QPushButton(potg_main)
        self.create_server_button.setObjectName("create_server_button")
        self.verticalLayout.addWidget(self.create_server_button)
        self.join_server_button = QtWidgets.QPushButton(potg_main)
        self.join_server_button.setObjectName("join_server_button")
        self.verticalLayout.addWidget(self.join_server_button)
        self.exit_game_button = QtWidgets.QPushButton(potg_main)
        self.exit_game_button.setObjectName("exit_game_button")
        self.verticalLayout.addWidget(self.exit_game_button)

        self.retranslateUi(potg_main)
        QtCore.QMetaObject.connectSlotsByName(potg_main)

    def retranslateUi(self, potg_main):
        _translate = QtCore.QCoreApplication.translate
        potg_main.setWindowTitle(_translate("potg_main", "Form"))
        self.create_server_button.setText(_translate("potg_main", "Create Server"))
        self.join_server_button.setText(_translate("potg_main", "Join Server"))
        self.exit_game_button.setText(_translate("potg_main", "Exit"))



class Ui_select_character_menu(object):
    def setupUi(self, potg_main):
        potg_main.setObjectName("potg_main")
        potg_main.resize(327, 320)
        self.verticalLayout = QtWidgets.QVBoxLayout(potg_main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.create_server_button = QtWidgets.QPushButton(potg_main)
        self.create_server_button.setObjectName("create_server_button")
        self.verticalLayout.addWidget(self.create_server_button)
        self.join_server_button = QtWidgets.QPushButton(potg_main)
        self.join_server_button.setObjectName("join_server_button")
        self.verticalLayout.addWidget(self.join_server_button)
        self.exit_game_button = QtWidgets.QPushButton(potg_main)
        self.exit_game_button.setObjectName("exit_game_button")
        self.verticalLayout.addWidget(self.exit_game_button)

        self.retranslateUi(potg_main)
        QtCore.QMetaObject.connectSlotsByName(potg_main)

    def retranslateUi(self, potg_main):
        _translate = QtCore.QCoreApplication.translate
        potg_main.setWindowTitle(_translate("potg_main", "Form"))
        self.create_server_button.setText(_translate("potg_main", "Chris Lee"))
        self.join_server_button.setText(_translate("potg_main", "Brodude"))
        self.exit_game_button.setText(_translate("potg_main", "Exit"))

