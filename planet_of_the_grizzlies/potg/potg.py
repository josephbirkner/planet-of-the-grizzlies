#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.curdir+"/network/"))
sys.path.append(os.path.abspath(os.curdir+"/views/"))
sys.path.append(os.path.abspath(os.curdir+"/util/"))
sys.path.append(os.path.abspath(os.curdir+"/world/"))
sys.path.append(os.path.abspath(os.curdir+"/controllers/"))

from potg_world import *
from potg_main_controller import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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

        self.main_menu = MainMenu(self.graphics)
        self.main_menu.signalExit.connect(self.deleteLater)

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

    def eventFilter(self, obj, e):
        if e.type() == QEvent.KeyPress and e.key() == Qt.Key_Escape:
            self.close()
            self.deleteLater()
        return QObject.eventFilter(self, obj, e)

block_size = (41, 40)

app = QApplication(sys.argv)

world = World("grizzlycity", block_size[0], block_size[1])
view = PlanetOfTheGrizzlies()
view.set_world(world)
world.signalPlayerPosChanged.connect(view.onPlayerPosChanged)
app.installEventFilter(view)

#QTimer.singleShot(200, view.showFullScreen)

sys.exit(app.exec_())
