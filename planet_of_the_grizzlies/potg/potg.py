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
from potg_ingame_controller import *
from potg_server import *
from potg_client import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import QGLWidget


class PlanetOfTheGrizzlies(QWidget):

    world = None

    local_server = None
    local_client = None

    main_menu = None
    ingame_menu = None
    dummy_scene = None

    def __init__(self):
        super().__init__()
        self.initUI()

    # user interface
    def initUI(self):
        self.graphics = QGraphicsView()
        self.graphics.resize(self.graphics.sizeHint())
        self.graphics.move(0, 0)
        self.graphics.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setStyleSheet("QGraphicsView { border-style: none; }")
        self.graphics.setViewport(QOpenGLWidget(self.graphics))

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphics, 0, 0)

        self.dummy_scene = QGraphicsScene()
        self.dummy_scene.setBackgroundBrush(QBrush(Qt.black))
        self.graphics.setScene(self.dummy_scene)

        self.ingame_menu = IngameMenu(self.graphics)
        self.ingame_menu.hide()

        self.main_menu = MainMenu(self.graphics)
        self.main_menu.signalExit.connect(self.deleteLater)
        self.main_menu.signalCreateServer.connect(self.onCreateServer)
        self.main_menu.show()

        self.setLayout(layout)
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('Planet Of The Grizzlies')
        self.show()

        self.resize_widgets()

    def set_world(self, world):
        self.world = world
        self.graphics.setScene(world)
        self.world.signalPlayerStatusChanged.connect(self.onPlayerStatusChanged)
        self.world.signalPlayerPosChanged.connect(self.onPlayerPosChanged)

    def onPlayerPosChanged(self, pos: QPointF):
        view_center = self.graphics.rect().center()
        pos_in_view_coords = self.graphics.mapFromScene(self.world.root.mapToScene(pos))
        dCx = pos_in_view_coords.x() - view_center.x()
        dCy = pos_in_view_coords.y() - view_center.y()

        scene_rect = self.world.root.childrenBoundingRect()
        scroll_pos = self.world.root.mapFromScene(self.graphics.mapToScene(QPoint(0, 0)))

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
            self.world.root.moveBy(-dCx, -dCy)
            self.world.scroll_background(self.world.player)

    def onPlayerStatusChanged(self, status):
        self.world.stop_updates()
        banner = None
        if status == 1:
            banner = self.world.addPixmap(QPixmap("gfx/win.png"))
        elif status == -1:
            banner = self.world.addPixmap(QPixmap("gfx/dead.png"))
        banner.setZValue(10)
        banner.setPos(self.graphics.viewport().width()/2-banner.pixmap().width()/2, self.graphics.viewport().height()/2-banner.pixmap().height()/2)

    def onClientLevelChanged(self):
        self.set_world(self.local_client.world)

    def onCreateServer(self):
        self.local_server = LocalServer()
        self.local_client = Client(self.local_server)
        self.local_client.signalLevelChanged.connect(self.onClientLevelChanged)
        view.local_server.request_level("grizzlycity_with_background")
        self.ingame_menu.show()
        self.main_menu.hide()
        self.resize_widgets()

    def eventFilter(self, obj, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == Qt.Key_Escape:
                self.close()
                self.deleteLater()
            elif self.local_server:
                self.local_server.notify_input(self.local_client.id, e.key(), True)
                # immediate application to the client in order to mitigate the lag of the server
                player = self.world.player_for_client(self.local_client.id)
                if player:
                    player.process_input(e.key, True)
            return True
        elif e.type() == QEvent.KeyRelease:
            self.local_server.notify_input(self.local_client.id, e.key(), False)
            # immediate application to the client in order to mitigate the lag of the server
            player = self.world.player_for_client(self.local_client.id)
            if player:
                player.process_input(e.key, False)
            return True
        return QObject.eventFilter(self, obj, e)

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        self.resize_widgets()

    def resize_widgets(self):
        if self.ingame_menu.isVisible():
            self.ingame_menu.resize(self.graphics.size())

        if self.main_menu.isVisible():
            menu_size = self.main_menu.size()
            self.main_menu.move(self.graphics.width()/2-menu_size.width()/2, self.graphics.height()/2-menu_size.height()/2)


app = QApplication(sys.argv)
view = PlanetOfTheGrizzlies()

app.installEventFilter(view)

#QTimer.singleShot(200, view.showFullScreen)

sys.exit(app.exec_())