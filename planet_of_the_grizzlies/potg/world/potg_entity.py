
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *


class Entity(QGraphicsPixmapItem):

    id = 0
    size = [0, 0, 0]
    logic_pos = [0, 0, 0]
    is_mirrored = False
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

    health = 100
    concentrate = 0

    Idle = 0
    Walking = 1
    Running = 2
    Dodging = 3
    Jumping = 4
    Punching = 5
    Punched = 6
    Kicking = 7
    Kicked = 8

    state = Idle

    sprites = None

    def __init__(self, id, pos, world, filename):
        super().__init__(QPixmap(filename).scaled(self.size[0], self.size[1]), world.root)
        self.id = id
        self.world = world
        self.logic_pos = [pos[0], pos[1], 0]
        self.velocity = [0, 0, 0]
        self.update_screen_pos()
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        # dictionary from the state of the entity to the its image
        self.sprites = {}
        self.load_images()

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

    def entity_type(self):
        return "Ent"

    def update(self):
        self.velocity[1] += self.world.gravity
        self.logic_pos[0] += self.velocity[0]
        self.logic_pos[1] += self.velocity[1]
        self.logic_pos[2] += self.velocity[2]
        if self.logic_pos[2] > self.world.depth - self.box.depth():
            self.logic_pos[2] = self.world.depth - self.box.depth()
        elif self.logic_pos[2] < 0:
            self.logic_pos[2] = 0
        if not self.platform or not self.platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
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
        for platform in self.world.platforms:
            if platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
                delta_y = platform.box.top() - self.logic_pos[1]
                if delta_y > 0 and (delta_y < best_delta_y or best_delta_y == -1):
                    best_delta_y = delta_y
                    best_platform = platform
        self.platform = best_platform

    # state of the movement
    def update_state(self, state):
        self.state = state
        self.setPixmap(self.sprites[state])
        self.is_mirrored = False
        self.resetTransform()
        if self.is_mirrored != (self.velocity[0] < 0):
            current_transform = self.transform()
            current_transform.scale(-1, 1)
            current_transform.translate(-self.boundingRect().width(), 0)
            self.setTransform(current_transform)
            self.is_mirrored = not self.is_mirrored

    def check_collision(self, object):
        if self.box.intersects(object.box):
            object.collision(self)
        self.update_screen_pos()

    def collision(self, colliding_entity):
        pass

    def serialize(self):
        result = {}
        result["pos"] = self.logic_pos[0:]
        result["velocity"] = self.velocity[0:]
        result["type"] = self.entity_type()
        result["id"] = self.id
        result["state"] = self.state
        return result

    def deserialize(self, json_data):
        assert json_data["id"] == self.id and json_data["type"] == self.entity_type()
        self.logic_pos = json_data["pos"]
        self.velocity = json_data["velocity"]
        if not self.platform or not self.platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
            self.update_platform()
        self.update_screen_pos()
        self.update_state(json_data["state"])

    def load_images(self):
        pass

    def attacking(self):
        self.concentrate += 10
        pass

    def attacked(self):
        self.health -= 10
        pass
