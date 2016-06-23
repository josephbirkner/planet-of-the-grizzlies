
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from potg_entity import *


class Player(Entity):

    size = [140, 84, 10]

    def __init__(self, pos, world):
        super().__init__(0, pos, world, "gfx/move_walk_player.png")

    def process_input(self, key, key_status):
        if key_status:
            if key == Qt.Key_Space and self.on_ground:
                self.velocity[1] += self.jump_strength
                self.on_ground = False
            # Walk
            elif key == Qt.Key_A:
                self.velocity[0] = -self.speed
            elif key == Qt.Key_D:
                self.velocity[0] = self.speed
            elif key == Qt.Key_W:
                self.velocity[2] = -self.speed
            elif key == Qt.Key_S:
                self.velocity[2] = self.speed
            # Punch
            elif key == Qt.Key_Up:
                pass
            # Kick
            elif key == Qt.Key_Down:
                pass
            elif key == Qt.Key_E:
                self.using = True
        else:
            if key == Qt.Key_A and self.velocity[0] < 0:
                self.velocity[0] = 0
            elif key == Qt.Key_D and self.velocity[0] > 0:
                self.velocity[0] = 0
            elif key == Qt.Key_W and self.velocity[2] < 0:
                self.velocity[2] = 0
            elif key == Qt.Key_S and self.velocity[2] > 0:
                self.velocity[2] = 0
            elif key == Qt.Key_E:
                self.using = False

    def entity_type(self):
        return "P"
