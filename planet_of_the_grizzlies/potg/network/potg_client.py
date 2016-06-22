
from potg_world import *

import uuid

class Client(QObject):

    world = None
    server = None
    id = 0

    signalLevelChanged = pyqtSignal()

    def __init__(self, server):
        super().__init__()
        self.id = str(uuid.uuid1())
        self.server = server
        server.add_client(self)

    def notify_world_update(self, updated_objects):
        assert self.world
        self.world.update_entities_from_list(updated_objects)

    def notify_level(self, level):
        self.world = World(level)
        self.signalLevelChanged.emit()


