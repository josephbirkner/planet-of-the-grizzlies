
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_main import *

class MainMenu(QWidget, Ui_potg_main):

    signalExit = pyqtSignal()
    signalCreateServer = pyqtSignal()
    signalJoinServer = pyqtSignal()

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        Ui_potg_main.__init__(self)
        self.setupUi(self)
        self.exit_game_button.mouseReleaseEvent = lambda e: self.signalExit.emit()
        self.create_server_button.mouseReleaseEvent = lambda e: self.signalCreateServer.emit()
        self.join_server_button.mouseReleaseEvent = lambda e: self.signalJoinServer.emit()