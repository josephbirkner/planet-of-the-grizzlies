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
    entities = []
    block_size = (0, 0)
    player = None
    gravity = .8
    depth_vec = (0, 0)
    depth = 0
    root = None
    update_timer_id = 0

    # signals
    signalPlayerPosChanged = pyqtSignal(QPointF)
    signalPlayerStatusChanged = pyqtSignal(int)

    def __init__(self, level, block_width, block_height, depth_vec=[122, 72], depth=10):
        super().__init__()

        # normalize depth vector
        self.depth = math.sqrt(depth_vec[0]*depth_vec[0] + depth_vec[1]*depth_vec[1]) # *float(block_width)
        self.depth_vec = depth_vec
        self.block_size = (block_width, block_height)

        self.root = QGraphicsRectItem()
        self.root.setPen(QPen(Qt.NoPen))
        self.root.setPos(0, 0)
        self.addItem(self.root)

        pos = [0, 0, 0]
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
                        self.blocks.append(Block(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "T":
                        self.blocks.append(TargetBlock(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "W":
                        self.blocks.append(Water(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "L":
                        self.blocks.append(Lever(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "P":
                        self.player = Player(pos[0:], self)
                        last = None
                    elif block == "E":
                        self.entities.append(Enemy(pos[0:], self))
                        last = None
                    else:
                        last = None

                pos[0] += block_width
            pos[1] += block_height

        # sort block by distance from camera
        self.blocks.sort(key=lambda block: (block.logic_pos[1], block.logic_pos[0]), reverse=True)
        for z in range(0, len(self.blocks)):
            self.blocks[z].setZValue(z)

        self.setFocusItem(self.player)

        # begin updates
        self.update_timer_id = self.startTimer(20)

    def timerEvent(self, e):
        # update all entities
        for ent in self.entities:
            ent.update()
        self.player.update()

        # check collision between player and entities
        for ent in self.entities:
            self.player.check_collision(ent)

        # check collision between entities and blocks
        for block in self.blocks:
            self.player.check_collision(block)
            for ent in self.entities:
                ent.check_collision(block)

        self.update_entity_zorder()
        self.signalPlayerPosChanged.emit(self.player.pos())

    def update_entity_zorder(self):
        for ent in self.entities+[self.player]:
            for block in self.blocks:
                if (ent.logic_pos[1], ent.logic_pos[0]) > (block.logic_pos[1], block.logic_pos[0]):
                    ent.setZValue(block.zValue()-.5)
                    break

    def stop_updates(self):
        self.killTimer(self.update_timer_id)


class PlanetOfTheGrizzlies(QWidget):

    world = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.graphics = QGraphicsView()
        self.graphics.resize(self.graphics.sizeHint())
        self.graphics.move(0, 0)
        self.graphics.setBackgroundBrush(Qt.black)
        self.graphics.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setStyleSheet("QGraphicsView { border-style: none; }")
        self.graphics.setViewport(QOpenGLWidget(self.graphics))

        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.graphics, 0, 0)

        self.setLayout(layout)
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('Planet Of The Grizzlies')
        self.show()

    def set_world(self, world):
        self.world = world
        self.graphics.setScene(world)
        self.world.signalPlayerStatusChanged.connect(self.onPlayerStatusChanged)

    def onPlayerPosChanged(self, pos: QPointF):
        view_center = self.graphics.rect().center()
        pos_in_view_coords = self.graphics.mapFromScene(world.root.mapToScene(pos))
        dCx = pos_in_view_coords.x() - view_center.x()
        dCy = pos_in_view_coords.y() - view_center.y()

        scene_rect = self.world.root.childrenBoundingRect()
        scroll_pos = world.root.mapFromScene(self.graphics.mapToScene(QPoint(0, 0)))

        if dCx < 0:
            edge_dist = scroll_pos.x()
            if edge_dist < abs(dCx):
                dCx = -edge_dist
        elif dCx > 0:
            edge_dist = scene_rect.width() - self.graphics.viewport().width() - scroll_pos.x()
            if edge_dist < dCx:
                dCx = edge_dist

        #if dCy < 0:
        #    edge_dist = scroll_pos.y()
        #    if edge_dist < abs(dCy):
        #        dCy = -edge_dist
        #elif dCy > 0:
        #    edge_dist = scene_rect.height() - self.graphics.viewport().height() - scroll_pos.y()
        #    if edge_dist < dCy:
        #        dCy = edge_dist

        if abs(dCx) > 0 or abs(dCy) > 0:
            world.root.moveBy(-dCx, -dCy)

    def onPlayerStatusChanged(self, status):
        self.world.stop_updates()
        banner = None
        if status == 1:
            banner = self.world.addPixmap(QPixmap("win.png"))
        elif status == -1:
            banner = self.world.addPixmap(QPixmap("dead.png"))
        banner.setPos(self.graphics.viewport().width()/2-banner.pixmap().width()/2, self.graphics.viewport().height()/2-banner.pixmap().height()/2)
        pass


level = [
    "____     ____                                         ",
    "L                                                     ",
    "            E                                         ",
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
    " P                        E                           ",
    "                          _                          _",
    "                     _                          _     ",
    "                                                      ",
    "_____          _           _____          _           ",
    "           ___                        ___             ",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# level = [
#     "___",
#     "   ",
#     " P "
# ]

block_size = (41, 40)

app = QApplication(sys.argv)

world = World(level, block_size[0], block_size[1])
view = PlanetOfTheGrizzlies()
view.set_world(world)
world.signalPlayerPosChanged.connect(view.onPlayerPosChanged)

QTimer.singleShot(200, view.showFullScreen)

sys.exit(app.exec_())