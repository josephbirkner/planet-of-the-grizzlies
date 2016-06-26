
from PyQt5.QtNetwork import *

from potg_world import *


class IServer(QObject):

    clients = {} # map from clientid to Client object
    heartbeat_timer_id = None

    # client-side methods

    def __init__(self):
        super(IServer, self).__init__()
        self.clients = {}
        self.heartbeat_timer_id = self.startTimer(100)

    def add_client(self, client):
        pass

    def remove_client(self, clientid):
        pass

    def request_level(self, level):
        pass

    def request_new_player(self, clientid):
        pass

    def notify_input(self, clientid, key, status):
        pass

    # server-side methods

    def timerEvent(self, e: QTimerEvent):
        pass

    def broadcast_update(self, updated_objects):
        pass

    def broadcast_level(self, level):
        pass

    def broadcast_to_remote_severs(self, message):
        pass


class LocalServer(IServer):

    world = None
    server = None

    # client-side methods

    def add_client(self, client):
        self.clients[client.id] = client
        self.server = QTcpServer()
        if not self.server.listen(QHostAddress("127.0.0.1")):
            print("server.listen() failed!")
            raise BaseException

    def remove_client(self, clientid):
        self.clients.pop(clientid)

    def request_level(self, level):
        self.world = World(level)
        self.broadcast_level(level)

    def request_new_player(self, clientid):
        if self.world:
            self.world.add_player(clientid)

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
            self.broadcast_update(changed_objects)

    def broadcast_update(self, updated_objects):
        for clientid, client in self.clients.items():
            client.notify_world_update(updated_objects, )
        #self.broadcast_to_remote_severs(json(updated_objects))

    def broadcast_level(self, level):
        for clientid, client in self.clients.items():
            client.notify_level(level)
        #self.broadcast_to_remote_severs(json(level))

    def broadcast_to_remote_severs(self, message):
        # for remote_server in self.remote_severs:
        #   remote_server.send(message)
        pass


class RemoteServer(IServer):

    socket = None

    def __init__(self, ip, port):            #ip and port of localserver
        super().__init__()
        socket = QTcpSocket()
        socket.connectToHost(ip, port)
        if not socket.waitForConnected(5000):
            print("Failed to connect to",ip,"at port",port)
            raise BaseException

    def add_client(self, client):
        pass

    def remove_client(self, clientid):
        pass

    def request_level(self, level):
        pass

    def request_new_player(self, clientid):
        pass

    def notify_input(self, clientid, key, status):
        pass

    # server-side methods

    def timerEvent(self, e: QTimerEvent):
        pass

    def broadcast_update(self, updated_objects):
        pass

    def broadcast_level(self, level):
        pass

    def broadcast_to_remote_severs(self, message):
        pass
