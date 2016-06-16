
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *


class Entity(QGraphicsPixmapItem):

    size = [0, 0, 0]
    logic_pos = [0, 0, 0]
    sprite = None
    status = 0
    velocity = [0, 0, 0]
    jump_strength = -18
    speed = 12
    on_ground = False
    using = False
    world = None
    box = None
    platform = None

    def __init__(self, pos, world, filename):
        super().__init__(QPixmap(filename).scaled(self.size[0], self.size[1]), world.root)
        self.world = world
        self.logic_pos = [pos[0], pos[1], 0]
        self.velocity = [0, 0, 0]
        self.update_screen_pos()
        self.setFlag(QGraphicsItem.ItemIsFocusable)

    def check_collision(self, object):
        if self.box.intersects(object.box):
            object.collision(self)
        self.update_screen_pos()

    def win(self):
        self.status = 1
        self.world.signalPlayerStatusChanged.emit(self.status)

    def kill(self):
        self.status = -1
        self.world.signalPlayerStatusChanged.emit(self.status)

    def won(self):
        return self.status == 1

    def killed(self):
        return self.status == -1

    def update(self):
        self.velocity[1] += self.world.gravity
        self.logic_pos[0] += self.velocity[0]
        self.logic_pos[1] += self.velocity[1]
        self.logic_pos[2] += self.velocity[2]
        if self.logic_pos[2] > self.world.depth - self.box.depth():
            self.logic_pos[2] = self.world.depth - self.box.depth()
        elif self.logic_pos[2] < 0:
            self.logic_pos[2] = 0
        if self.platform is None or not self.platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
            self.update_platform()
        self.update_screen_pos()

    def update_screen_pos(self):
        screen_pos = self.logic_pos[0:]
        screen_pos[0] += self.logic_pos[2]/self.world.depth * self.world.depth_vec[0]
        screen_pos[1] += self.logic_pos[2]/self.world.depth * self.world.depth_vec[1]
        self.setPos(screen_pos[0], screen_pos[1])
        self.box = Box(self.logic_pos, self.size)

    def update_platform(self):
        best_delta_y = -1
        best_platform = None
        for platform in self.world.blocks:
            if platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
                delta_y = platform.box.top() - self.logic_pos[1]
                if delta_y > 0 and (delta_y < best_delta_y or best_delta_y == -1):
                    best_delta_y = delta_y
                    best_platform = platform
        self.platform = best_platform

    def collision(self, colliding_entity):
        pass

    def entity_type(self):
        return "Ent"

