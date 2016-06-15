
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_main import *

class MainMenu(QWidget, Ui_MainMenu):

    signalExit = pyqtSignal()

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        Ui_MainMenu.__init__(self)
        self.setupUi(self)
        self.exitButton.mouseReleaseEvent = self.onExitButtonClicked

    def onExitButtonClicked(self, e):
        self.signalExit.emit()
