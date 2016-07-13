
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from potg_entity import *


class Player(Entity):

    size = [349/3, 374/3, 50]
    concentrate = 0
    punch_strength = 5
    kick_strength = 5
    clientid = ""
    appearance = 1
    max_health = 100

    def __init__(self, pos, world, clientid, appearance):
        self.appearance = appearance
        self.clientid = clientid
        self.health = self.max_health
        super().__init__(0, pos, world, "gfx/walk_player.png")

    def process_input(self, key, key_status):
        if key_status:
            if key == Qt.Key_Space and self.on_ground:
                self.velocity[1] += self.jump_strength
                self.on_ground = False
                self.activate_state(Entity.Jumping)
            elif key == Qt.Key_A:
                self.velocity[0] = -self.speed
                self.activate_state(Entity.Walking)
            elif key == Qt.Key_D:
                self.velocity[0] = self.speed
                self.activate_state(Entity.Walking)
            elif key == Qt.Key_W:
                self.velocity[2] = -self.speed
                self.activate_state(Entity.Walking)
            elif key == Qt.Key_S:
                self.velocity[2] = self.speed
                self.activate_state(Entity.Walking)
            elif key == Qt.Key_Up:
                self.activate_state(Entity.Punching)
            elif key == Qt.Key_Down:
                self.activate_state(Entity.Kicking)
            elif key == Qt.Key_E:
                self.using = True
        else:
            if key == Qt.Key_Space:
                self.deactivate_state(Entity.Jumping)
            elif key == Qt.Key_A and self.velocity[0] < 0:
                self.velocity[0] = 0
                self.deactivate_state(Entity.Walking)
            elif key == Qt.Key_D and self.velocity[0] > 0:
                self.velocity[0] = 0
                self.deactivate_state(Entity.Walking)
            elif key == Qt.Key_W and self.velocity[2] < 0:
                self.velocity[2] = 0
                self.deactivate_state(Entity.Walking)
            elif key == Qt.Key_S and self.velocity[2] > 0:
                self.velocity[2] = 0
                self.deactivate_state(Entity.Walking)
            elif key == Qt.Key_E:
                self.using = False
            # stopping punching upon punching
            elif key == Qt.Key_Up:
                self.deactivate_state(Entity.Punching)
            elif key == Qt.Key_Down and self.state == Entity.Kicking:
                self.deactivate_state(Entity.Kicking)

    def entity_type(self):
        return "P"

    def load_images(self):
        if self.appearance == 0:
            self.sprites[Entity.Idle] = [QPixmap("gfx/player_idle.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Walking] = [QPixmap("gfx/player_step1.png").scaled(self.size[0], self.size[1]), QPixmap("gfx/player_step2.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Punching] = [QPixmap("gfx/player_punch.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Jumping] = [QPixmap("gfx/player_jump.png").scaled(self.size[0], self.size[1])]
            #self.sprites[Entity.Punched] = [QPixmap("gfx/punch_enemy.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Kicking] = [QPixmap("gfx/player_kick.png").scaled(self.size[0], self.size[1])]
            #self.sprites[Entity.Kicked] = [QPixmap("gfx/kick_enemy.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Dead] = [QPixmap("gfx/player_idle.png").scaled(self.size[0], self.size[1])]
        else:
            self.sprites[Entity.Idle] = [QPixmap("gfx/brodude_idle.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Walking] = [QPixmap("gfx/brodude_step1.png").scaled(self.size[0], self.size[1]),
                                            QPixmap("gfx/brodude_step2.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Jumping] = [QPixmap("gfx/brodude_jump.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Punching] = [QPixmap("gfx/brodude_attack1.png").scaled(self.size[0], self.size[1])]
            # self.sprites[Entity.Punched] = [QPixmap("gfx/punch_enemy.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Kicking] = [QPixmap("gfx/brodude_attack2.png").scaled(self.size[0], self.size[1])]
            # self.sprites[Entity.Kicked] = [QPixmap("gfx/kick_enemy.png").scaled(self.size[0], self.size[1])]
            self.sprites[Entity.Dead] = [QPixmap("gfx/brodude_idle.png").scaled(self.size[0], self.size[1])]


    def on_state_transition(self, old_state, new_state):
        self.world.signalPlayerStatusChanged.emit(self.clientid, new_state)

    def serialize(self):
        result = super().serialize()
        result["clientid"] = self.clientid
        result["appearance"] = self.appearance
        return result
