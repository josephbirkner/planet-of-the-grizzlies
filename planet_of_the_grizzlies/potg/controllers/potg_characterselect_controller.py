
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import potg_characterselect


class CharacterselectMenu(QWidget, potg_characterselect.Ui_Form):

    signalCancel = pyqtSignal()
    signalAccept = pyqtSignal(int)

    selected_character = 0

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        potg_characterselect.Ui_Form.__init__(self)
        self.setupUi(self)

        self.player_1_button.mouseReleaseEvent = lambda e: self.onSelectCharacter(0)
        self.player_2_button.mouseReleaseEvent = lambda e: self.onSelectCharacter(1)
        self.select_button.mouseReleaseEvent = lambda e: self.onAcceptButtonClicked()
        self.cancel_button.mouseReleaseEvent = lambda e: self.signalCancel.emit()
        self.player_1_button.setIcon(QIcon(QPixmap("gfx/player_idle.png").scaled(200, 200)))
        self.player_1_button.setIconSize(QSize(200, 200))
        self.player_2_button.setIcon(QIcon(QPixmap("gfx/brodude.png").scaled(200, 200)))
        self.player_2_button.setIconSize(QSize(200, 200))

    def onSelectCharacter(self, index):
        self.selected_character = index
        if index == 0:
            self.player_1_button.setChecked(True)
            self.player_2_button.setChecked(False)
        elif index == 1:
            self.player_1_button.setChecked(False)
            self.player_2_button.setChecked(True)

    def onAcceptButtonClicked(self):
        self.signalAccept.emit(self.selected_character)

