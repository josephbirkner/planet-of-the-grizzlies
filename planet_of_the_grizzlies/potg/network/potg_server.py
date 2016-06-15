
from potg_world import *

class IServer(QObject):

    clients = {} # map from clientid to Client object
    heartbeat_timer_id = None

    # client-side methods

    def __init__(self):
        super(IServer, self).__init__()
        self.clients = {}
        self.heartbeat_timer_id = self.startTimer(50)

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

    def broadcast(self, message):
        pass


class LocalServer(IServer):

    world = None

    # client-side methods

    def add_client(self, client):
        self.clients[client.id()] = client

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
        if not self.world:
            changed_objects = self.world.changed_entities():
            self.world.reset_changed_entities()


    def broadcast_update(self, updated_objects):
        pass

    def broadcast_level(self, level):
        pass

    def broadcast(self, message):
        pass
