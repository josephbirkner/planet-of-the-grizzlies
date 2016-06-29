
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from potg_entity import *


class Player(Entity):

    size = [140, 84, 10]

    def __init__(self, pos, world):
        super().__init__(0, pos, world, "gfx/walk_player.png")

    def process_input(self, key, key_status):
        if key_status:
            if key == Qt.Key_Space and self.on_ground:
                self.velocity[1] += self.jump_strength
                self.on_ground = False
            elif key == Qt.Key_A:
                self.velocity[0] = -self.speed
            elif key == Qt.Key_D:
                self.velocity[0] = self.speed
            elif key == Qt.Key_W:
                self.velocity[2] = -self.speed
            elif key == Qt.Key_S:
                self.velocity[2] = self.speed
            elif key == Qt.Key_Up:
                self.update_state(Entity.Punching)
            elif key == Qt.Key_Down:
                self.update_state(Entity.Kicking)
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
            # stopping punching upon punching
            elif key == Qt.Key_Up and self.state == Entity.Punching:
                self.update_state(Entity.Idle)
            elif key == Qt.Key_Down and self.state == Entity.Kicking:
                self.update_state(Entity.Idle)


    def entity_type(self):
        return "P"

    def load_images(self):
        self.sprites[Entity.Idle] = QPixmap("gfx/walk_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Walking] = QPixmap("gfx/walk_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Running] = QPixmap("gfx/walk_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Dodging] = QPixmap("gfx/walk_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Jumping] = QPixmap("gfx/walk_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Punching] = QPixmap("gfx/punch_player.png").scaled(self.size[0], self.size[1])
        #self.sprites[Entity.Punched] = QPixmap("gfx/punch_enemy.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Kicking] = QPixmap("gfx/kick_player.png").scaled(self.size[0], self.size[1])
        #self.sprites[Entity.Kicked] = QPixmap("gfx/kick_enemy.png").scaled(self.size[0], self.size[1])
