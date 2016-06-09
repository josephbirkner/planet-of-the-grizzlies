
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from potg_entity import *


class Player(Entity):

    size = [140, 84, 10]

    def __init__(self, pos, world):
        super().__init__(pos, world, "gfx/grizzlie.png")

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Space and self.on_ground:
            self.velocity[1] += self.jump_strength
            self.on_ground = False
        elif e.key() == Qt.Key_Left:
            self.velocity[0] = -self.speed
        elif e.key() == Qt.Key_Right:
            self.velocity[0] = self.speed
        elif e.key() == Qt.Key_Up:
            self.velocity[2] = -self.speed
        elif e.key() == Qt.Key_Down:
            self.velocity[2] = self.speed
        elif e.key() == Qt.Key_E:
            self.using = True

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Left and self.velocity[0] < 0:
            self.velocity[0] = 0
        elif e.key() == Qt.Key_Right and self.velocity[0] > 0:
            self.velocity[0] = 0
        elif e.key() == Qt.Key_Up and self.velocity[2] < 0:
            self.velocity[2] = 0
        elif e.key() == Qt.Key_Down and self.velocity[2] > 0:
            self.velocity[2] = 0
        elif e.key() == Qt.Key_E:
            self.using = False

    def entity_type(self):
        return "P"

