
from potg_world import *

import uuid

class Client(QObject):

    world = None
    server = None
    id = 0

    signalLevelChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid1())

    def notify_world_update(self, updated_objects, level):
        if not self.world:
            self.notify_level(level)
        assert self.world and self.world.name == level
        self.world.update_entities_from_list(updated_objects)

    def notify_level(self, level):
        if self.world:
            self.world.disconnect()
            self.world.deleteLater()
            del self.world
            self.world = None
        if level:
            self.world = World(level)
        self.signalLevelChanged.emit()

    def attach_to_server(self, server):
        if self.server and self.server != server:
            self.server.remove_client(self.id)
        self.server = server
        if self.server:
            self.server.add_client(self)


