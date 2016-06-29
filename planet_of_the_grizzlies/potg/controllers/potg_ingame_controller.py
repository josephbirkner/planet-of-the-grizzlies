
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_ingame import *

class IngameMenu(QWidget, Ui_potg_ingame):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        Ui_potg_ingame.__init__(self)
        self.setupUi(self)

    def onExitButtonClicked(self, e):
        self.signalExit.emit()
