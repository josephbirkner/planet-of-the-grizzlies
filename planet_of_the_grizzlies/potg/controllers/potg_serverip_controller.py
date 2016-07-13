
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import potg_serverip


class ServerIpMenu(QWidget, potg_serverip.Ui_potg_serverip):

    signalCancel = pyqtSignal()
    signalConnect = pyqtSignal(str)

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        potg_serverip.Ui_potg_serverip.__init__(self)
        self.setupUi(self)

        self.connect_button.mouseReleaseEvent = lambda e: self.onConnectButtonClicked()
        self.cancel_button.mouseReleaseEvent = lambda e: self.signalCancel.emit()

    def onConnectButtonClicked(self, e):
        self.signalConnect.emit(self.lineEdit.text())
