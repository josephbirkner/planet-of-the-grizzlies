
from PyQt5.QtNetwork import *
from os import remove

from potg_world import *
from potg_messages import *


class IServer(QObject):

    clients = {} # map from clientid to Client object
    heartbeat_timer_id = None

    # client-side methods

    def __init__(self):
        super(IServer, self).__init__()
        self.clients = {}
        self.heartbeat_timer_id = self.startTimer(100)

    def add_client(self, client):
        self.clients[client.id] = client

    def remove_client(self, clientid):
        self.clients.pop(clientid)

    def request_level(self, level):
        pass

    def request_new_player(self, clientid, appearance):
        pass

    def notify_input(self, clientid, key, status):
        pass

    # server-side methods

    def timerEvent(self, e: QTimerEvent):
        pass

    def broadcast_update(self, updated_objects, level):
        pass

    def broadcast_level(self, level):
        pass

    def broadcast_to_remote_severs(self, message):
        pass


class LocalServer(IServer):

    world = None
    server = None

    transition_active = False

    # map from QTcpSocket to list of client ids
    remote_servers = None

    # client-side methods

    def __init__(self):
        self.server = QTcpServer()
        if not self.server.listen(QHostAddress.Any, 27030):
            print("server.listen() failed!")
            raise BaseException
        super().__init__()
        self.server.newConnection.connect(self.on_new_connection)
        self.remote_servers = {}

    def request_level(self, level):
        if self.world:
            self.world.disconnect()
            self.world.deleteLater()
            del self.world
            self.world = None

        if level:
            self.world = World(level, World.DisableBackgrounds|World.DisablePlatformGraphics)
            self.world.signalPlayerStatusChanged.connect(self.on_player_status_changed)

        self.broadcast_level(level)

    def request_new_player(self, clientid, appearance):
        if self.world:
            self.world.add_player(clientid, appearance)

    def notify_input(self, clientid, key, status):
        if self.world:
            player = self.world.player_for_client(clientid)
            if player:
                player.process_input(key, status)

    # server-side methods

    def timerEvent(self, e: QTimerEvent):
        if self.world:
            changed_objects = self.world.changed_entities()
            self.world.reset_changed_entities()
            self.broadcast_update(changed_objects, self.world.name)

    def on_player_status_changed(self, clientid, status):
        if self.transition_active:
            return

        if status == Entity.Won:
            QTimer.singleShot(3000, self.transition_level)
            self.transition_active = True
        elif status == Entity.Dead:
            QTimer.singleShot(3000, self.leave_level)
            self.transition_active = False

    def transition_level(self):
        self.transition_active = False
        if self.world:
            self.request_level(self.world.nextlevel)

    def leave_level(self):
        self.transition_active = False
        if self.world:
            self.request_level(self.world.name)

    def on_new_connection(self):
        print("new connection!")
        remote_socket = self.server.nextPendingConnection()
        print(remote_socket.isOpen())
        remote_socket.readyRead.connect(self.on_ready_read)
        remote_socket.setSocketOption(QAbstractSocket.LowDelayOption, True)
        self.remote_servers[remote_socket] = []

    def on_ready_read(self):
        data = self.sender().readAll()
        data = data.data() # get the raw bytes from the QByteArray object
        self.sender().flush()
        try:
            data = data[1:-1]
            messages = data.split(b"}{")
            for data in messages:
                msg = Message.Parse(b"{%s}" % data)

                if msg.mtype == "add_client":
                    self.remote_servers[self.sender()].append(msg.value("clientid"))
                    if self.world:
                        self.sender().write(Message("level", {"name": self.world.name}).to_bytes())
                        self.sender().flush()

                elif msg.mtype == "request_player":
                    self.request_new_player(msg.value("clientid"), msg.value("appearance"))

                elif msg.mtype == "input":
                    self.notify_input(msg.value("clientid"), msg.value("key"), msg.value("status"))

        except json.JSONDecodeError as e:
            print(e.msg)

    def broadcast_update(self, updated_objects, level):
        for clientid, client in self.clients.items():
            client.notify_world_update(updated_objects, level)
        self.broadcast_to_remote_severs(Message("update", {"entities": updated_objects, "level": self.world.name}).to_bytes())

    def broadcast_level(self, level):
        for clientid, client in self.clients.items():
            client.notify_level(level)
        self.broadcast_to_remote_severs(Message("level", {"name":level}).to_bytes())

    def broadcast_to_remote_severs(self, message):
        for socket, clients in self.remote_servers.items():
            socket.write(message)
            socket.flush()


class RemoteServer(IServer):

    socket = QTcpSocket()

    def __init__(self, ip, port):            #ip and port of localserver
        super().__init__()
        self.socket = QTcpSocket()
        self.socket.connectToHost(ip, port)
        if not self.socket.waitForConnected(10000) or not self.socket.isOpen():
            print("Failed to connect to",ip,"at port",port)
            raise BaseException
        self.socket.readyRead.connect(self.on_ready_read)
        self.socket.setSocketOption(QAbstractSocket.LowDelayOption, True)

    def add_client(self, client):
        super().add_client(client)
        self.socket.write(ClientMessage("add_client", client.id).to_bytes())
        #self.socket.flush()

    def remove_client(self, clientid):
        super().remove_client(clientid)
        self.socket.write(ClientMessage("remove_client", clientid).to_bytes())
        #self.socket.flush()

    def request_level(self, level):
        pass

    def request_new_player(self, clientid, appearance):
        self.socket.write(ClientMessage("request_player", clientid, {"appearance": appearance}).to_bytes())
        #self.socket.flush()

    def notify_input(self, clientid, key, status):
        self.socket.write(ClientMessage("input", clientid, {"key": key, "status": status}).to_bytes())
        #self.socket.flush()

    # server-side methods

    def on_ready_read(self):
        data = self.socket.readAll()
        data = data.data() # get the raw bytes from the QByteArray object
        self.sender().flush()
        try:
            data = data[1:-1]
            messages = data.split(b"}{")
            for data in messages:
                msg = Message.Parse(b"{%s}" % data)

                if msg.mtype == "level":
                    self.broadcast_level(msg.value("name"))

                elif msg.mtype == "update":
                    self.broadcast_update(msg.value("entities"), msg.value("level"))

        except json.JSONDecodeError as e:
            print(e.msg)

    def broadcast_update(self, updated_objects, level):
        for clientid, client in self.clients.items():
            client.notify_world_update(updated_objects, level)

    def broadcast_level(self, level):
        for clientid, client in self.clients.items():
            client.notify_level(level)
