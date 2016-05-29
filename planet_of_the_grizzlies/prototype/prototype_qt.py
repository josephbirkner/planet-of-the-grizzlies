#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math
import os

sys.path.append(os.path.abspath(os.curdir))

from prototype_qt_blocks import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class World(QGraphicsScene):

    blocks = []
    block_size = (0, 0)
    player = None
    gravity = .8
    depth_vec = (0, 0)
    depth = 10

    def __init__(self, level, block_width, block_height, depth_vec=[2, 1], depth=10):
        super().__init__()

        # normalize depth vector
        depth_len = math.sqrt(depth_vec[0]*depth_vec[0] + depth_vec[1]*depth_vec[1]) # *float(block_width)
        depth_vec[0] /= depth_len
        depth_vec[1] /= depth_len

        self.depth_vec = depth_vec
        self.depth = depth
        self.block_size = (block_width, block_height)

        pos = [0, 0]
        self.width = len(level[0])
        self.height = len(level)
        for line in level:
            pos[0] = 0
            last = None
            for block in line:
                if last and block == last.item_type():
                    last.width_blocks += 1
                    last.notify_blocks_changed()
                else:
                    if block == "_":
                        self.blocks.append(Block((pos[0], pos[1]), self))
                        last = self.blocks[-1]
                    elif block == "T":
                        self.blocks.append(TargetBlock((pos[0], pos[1]), self))
                        last = self.blocks[-1]
                    elif block == "W":
                        self.blocks.append(Water((pos[0], pos[1]), self))
                        last = self.blocks[-1]
                    elif block == "L":
                        self.blocks.append(Lever((pos[0], pos[1]), self))
                        last = self.blocks[-1]
                    elif block == "P":
                        self.player = Player((pos[0], pos[1]), self)
                        self.addItem(self.player)
                        last = None
                    else:
                        last = None

                    if last:
                        self.addItem(last)

                pos[0] += block_width
            pos[1] += block_height

        # sort block by distance from camera
        self.blocks.sort(key=lambda block: (block.pos[1], block.pos[0]), reverse=True)
        for z in range(0, len(self.blocks)):
            self.blocks[z].setZValue(z)

        self.setFocusItem(self.player)

        # begin updates
        self.startTimer(20)

    def timerEvent(self, e):
        self.player.update()
        for block in self.blocks:
            self.player.check_collision(block)
        self.update_player_z_order()

    def update_player_z_order(self):
        for block in self.blocks:
            if (self.player.pos[1], self.player.pos[0]) > (block.pos[1], block.pos[0]):
                self.player.setZValue(block.zValue()+.5)
                break


class GameView(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(Qt.black)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class PlanetOfTheGrizzlies(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.graphics = GameView()
        self.graphics.resize(self.graphics.sizeHint())
        self.graphics.move(0, 0)

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.graphics, 0, 0)

        self.setLayout(layout)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Planet Of The Grizzlies')
        self.show()

    def set_world(self, world):
        self.graphics.setScene(world)


level = [
    "____                                                  ",
    "L                                                     ",
    "                                                      ",
    "                                                      ",
    "        _____                   ________              ",
    "            _                          _              ",
    "__          _               _          _              ",
    "            _                          _              ",
    "            _     _________            ________       ",
    "            ______                            _       ",
    "                                              _TTTTTTT",
    "                           _____              ________",
    "                                                      ",
    "____                                                  ",
    "                                                 L    ",
    "                                        _             ",
    " P                                                    ",
    "                          _                          _",
    "                     _                          _     ",
    "                                                      ",
    "_____          _           _____          _           ",
    "           ___                        ___             ",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

block_size = (42, 42)

app = QApplication(sys.argv)

world = World(level, block_size[0], block_size[1])
view = PlanetOfTheGrizzlies()
view.set_world(world)

sys.exit(app.exec_())