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
from potg_characterselect_controller import *
from potg_serverip_controller import *

from potg_server import *
from potg_client import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import QGLWidget

import qdarkstyle


class PlanetOfTheGrizzlies(QWidget):

    world = None

    server_type = False # False for RemoteServer, True fro LocalServer
    server = None
    client = None

    selected_player_appearance = 0

    main_menu = None
    character_menu = None
    serverip_menu = None
    ingame_menu = None

    dummy_scene = None
    banner = None

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
        self.graphics.setBackgroundBrush(QBrush(Qt.black))

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

        self.serverip_menu = ServerIpMenu(self.graphics)
        self.serverip_menu.signalCancel.connect(self.onCancelMenu)
        self.serverip_menu.signalConnect.connect(self.onConnectWithIp)
        self.serverip_menu.hide()

        self.character_menu = CharacterselectMenu(self.graphics)
        self.character_menu.signalCancel.connect(self.onCancelMenu)
        self.character_menu.signalAccept.connect(self.onSelectAppearance)
        self.character_menu.hide()

        self.setLayout(layout)
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('Planet Of The Grizzlies')
        self.show()

        self.resize_widgets()

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

        player = self.world.player_for_client(self.client.id)
        if player:
            self.ingame_menu.setCurrentHealth(player.health, player.max_health)

    def onPlayerStatusChanged(self, clientid, status):
        if self.banner is not None:
            return

        if status == Entity.Won:
            self.banner = self.world.addPixmap(QPixmap("gfx/win.png"))
        elif status == Entity.Dead:
            self.banner = self.world.addPixmap(QPixmap("gfx/dead.png"))

        if self.banner:
            self.banner.setZValue(1000)
            self.banner.setPos(self.graphics.viewport().width()/2-self.banner.pixmap().width()/2, self.graphics.viewport().height()/2-self.banner.pixmap().height()/2)

    def showMainMenu(self):
        self.main_menu.show()
        self.ingame_menu.hide()
        self.graphics.setScene(self.dummy_scene)

    #def showCharacterMenu(self):
    #    self.select_character.show()
    #    self.main_menu.hide()
    #   self.graphics.setScene(self.dummy_scene)

    def onClientLevelChanged(self):
        self.world = self.client.world
        self.banner = None
        if self.world:
            self.world.signalPlayerStatusChanged.connect(self.onPlayerStatusChanged)
            self.world.signalPlayerPosChanged.connect(self.onPlayerPosChanged)
            self.graphics.setScene(self.client.world)
            self.ingame_menu.show()
            self.main_menu.hide()
            self.serverip_menu.hide()
            self.character_menu.hide()
            self.resize_widgets()
            self.server.request_new_player(self.client.id, self.selected_player_appearance)
        else:
            self.showMainMenu()

    def onCreateServer(self):
        self.server_type = True
        self.main_menu.hide()
        self.character_menu.show()
        self.resize_widgets()

    def onJoinServer(self):
        self.server_type = False
        self.main_menu.hide()
        self.character_menu.show()
        self.resize_widgets()

    def onConnectWithIp(self, ip):
        self.server = RemoteServer(ip, 27030)
        self.client.attach_to_server(self.server)

    def onCancelMenu(self):
        self.serverip_menu.hide()
        self.character_menu.hide()
        self.main_menu.show()
        self.resize_widgets()

    def onSelectAppearance(self, appearance):
        self.selected_player_appearance = appearance
        if self.server_type:
            if type(self.server) != LocalServer:
                self.server = LocalServer()
                self.client.attach_to_server(self.server)
            #self.server.request_level("grizzlycity")
            #self.server.request_level("ninja_level")
            self.server.request_level("drevil")
        else:
            self.character_menu.hide()
            self.serverip_menu.show()
            self.resize_widgets()

    def eventFilter(self, obj, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == Qt.Key_Escape:
                self.close()
                self.deleteLater()
                return True
            elif e.key() == Qt.Key_Backspace and self.server:
                # self.server.request_new_player(self.client.id)
                self.server.request_level("drevil")
                return True
            elif self.server:
                self.server.notify_input(self.client.id, e.key(), True)
                # immediate application to the client in order to mitigate the lag of the server
                player = self.world.player_for_client(self.client.id)
                if player:
                    player.process_input(e.key, True)
                return True
        elif e.type() == QEvent.KeyRelease and self.server:
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

        if self.serverip_menu.isVisible():
            self.serverip_menu.resize(self.graphics.size())

        if self.character_menu.isVisible():
            self.character_menu.resize(self.graphics.size())

        if self.main_menu.isVisible():
            menu_size = self.main_menu.size()
            self.main_menu.move(self.graphics.width()/2-menu_size.width()/2, self.graphics.height()/2-menu_size.height()/2)


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet(False))

view = PlanetOfTheGrizzlies()

app.installEventFilter(view)

#QTimer.singleShot(200, view.showFullScreen)

sys.exit(app.exec_())