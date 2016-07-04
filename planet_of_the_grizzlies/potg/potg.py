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

import qdarkstyle


class PlanetOfTheGrizzlies(QWidget):

    world = None

    server = None
    client = None

    main_menu = None
    ingame_menu = None
    dummy_scene = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Client()
        self.client.signalLevelChanged.connect(self.onClientLevelChanged)

    # user interface
    def initUI(self):
        self.graphics = QGraphicsView()
        self.graphics.resize(self.graphics.sizeHint())
        self.graphics.move(0, 0)
        self.graphics.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics.setStyleSheet("QGraphicsView { border-style: none; }")
        self.graphics.setViewport(QOpenGLWidget())

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
        self.main_menu.signalJoinServer.connect(self.onJoinServer)
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
        if not self.world.player_for_client(self.client.id):
            self.server.request_new_player(self.client.id)

    def onPlayerPosChanged(self, clientid, pos: QPointF):
        if clientid != self.client.id:
            return

        view_center = self.graphics.rect().center()
        pos_in_view_coords = self.graphics.mapFromScene(self.world.root.mapToScene(pos))
        dCx = pos_in_view_coords.x() - view_center.x()
        dCy = pos_in_view_coords.y() - view_center.y()

        scene_rect = self.world.root.rect()
        scroll_pos = self.world.root.mapFromScene(self.graphics.mapToScene(QPoint(0, 0)))
        #scroll_pos = self.graphics.mapToScene(QPoint(0, 0))

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
            self.world.scroll_background(self.world.player_for_client(self.client.id))

    def onPlayerStatusChanged(self, clientid, status):
        banner = None

        if status == Entity.Won:
            banner = self.world.addPixmap(QPixmap("gfx/win.png"))
        elif status == Entity.Dead:
            banner = self.world.addPixmap(QPixmap("gfx/dead.png"))

        if banner:
            self.world.stop_updates()
            banner.setZValue(10)
            banner.setPos(self.graphics.viewport().width()/2-banner.pixmap().width()/2, self.graphics.viewport().height()/2-banner.pixmap().height()/2)

    def onClientLevelChanged(self):
        self.set_world(self.client.world)
        self.ingame_menu.show()
        self.main_menu.hide()
        self.resize_widgets()

    def onCreateServer(self):
        self.server = LocalServer()
        self.client.attach_to_server(self.server)
        self.server.request_level("grizzlycity_with_background")
        self.server.request_new_player(self.client.id)

    def onJoinServer(self):
        self.server = RemoteServer("127.0.0.1", 27030)
        self.client.attach_to_server(self.server)
        self.server.request_new_player(self.client.id)

    def eventFilter(self, obj, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == Qt.Key_Escape:
                self.close()
                self.deleteLater()
            elif e.key() == Qt.Key_Backspace and self.server:
                self.server.request_new_player(self.client.id)
            elif self.server:
                self.server.notify_input(self.client.id, e.key(), True)
                # immediate application to the client in order to mitigate the lag of the server
                player = self.world.player_for_client(self.client.id)
                if player:
                    player.process_input(e.key, True)
            return True
        elif e.type() == QEvent.KeyRelease:
            self.server.notify_input(self.client.id, e.key(), False)
            # immediate application to the client in order to mitigate the lag of the server
            player = self.world.player_for_client(self.client.id)
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
app.setStyleSheet(qdarkstyle.load_stylesheet(False))

view = PlanetOfTheGrizzlies()

app.installEventFilter(view)

#QTimer.singleShot(200, view.showFullScreen)

sys.exit(app.exec_())