#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class FourInARow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        graphics = Board()
        graphics.resize(graphics.sizeHint())
        graphics.move(0, 0)

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(graphics, 0, 0)

        self.setLayout(layout)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('VIER GEWINNT 3000')
        self.show()


class Board(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor(50, 90, 150)))

app = QApplication(sys.argv)
ex = FourInARow()
sys.exit(app.exec_())