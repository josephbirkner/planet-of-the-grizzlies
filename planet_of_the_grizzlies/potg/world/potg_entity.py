
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *


class Entity(QGraphicsPixmapItem):

    id = 0
    size = [0, 0, 0]
    logic_pos = [0, 0, 0]
    is_mirrored = False
    sprite = None
    velocity = [0, 0, 0]
    jump_strength = -18
    speed = 12
    on_ground = False
    using = False
    world = None
    box = None
    platform = None

    health = 100

    Idle = 0
    Walking = 1
    Running = 2
    Dodging = 3
    Jumping = 4
    Punching = 5
    Punched = 6
    Kicking = 7
    Kicked = 8
    Dead = 9
    Won = 10

    state = -1
    old_state = -1
    preserve_old_state_for_next_update = False

    sprites = None
    sprite_cycle_timer_interval = 8 # change image every 15 updates
    current_sprite_list = None
    current_sprite_list_index = 0
    update_count = 0

    state_updates = 0
    state_duration = 0
    fall_back_to_this_state_after_temporary_expired = Idle

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
        self.set_state(Entity.Idle)

    def killed(self):
        return self.state == Entity.Dead

    def entity_type(self):
        return "Ent"

    def update(self):
        self.update_count += 1
        self.update_count %= self.sprite_cycle_timer_interval

        if self.preserve_old_state_for_next_update:
            self.preserve_old_state_for_next_update = False
        else:
            self.old_state = self.state

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
        self.update_sprite()
        self.update_state()

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
    def set_state(self, state, duration=-1):
        self.state_updates = 0
        self.state_duration = duration

        if self.state != state:
            self.preserve_old_state_for_next_update = True
            self.old_state = self.state
            self.fall_back_to_this_state_after_temporary_expired = self.state
            self.state = state
            self.setPixmap(self.sprites[state][0])
            self.current_sprite_list = self.sprites[state]
            self.current_sprite_list_index = 0
            if not self.current_sprite_list:
                print("warning: attempt to set nonexsiting sprite for state",state)

        self.is_mirrored = False
        self.resetTransform()
        if self.is_mirrored != (self.velocity[0] < 0):
            current_transform = self.transform()
            current_transform.scale(-1, 1)
            current_transform.translate(-self.boundingRect().width(), 0)
            self.setTransform(current_transform)
            self.is_mirrored = not self.is_mirrored

    def update_state(self):
        self.state_updates += 1
        if self.state_updates >= self.state_duration and self.state_duration > 0:
            self.set_state(self.fall_back_to_this_state_after_temporary_expired)

    def update_sprite(self):
        if self.update_count == 0:
            self.current_sprite_list_index += 1
            self.current_sprite_list_index %= len(self.current_sprite_list)
            self.setPixmap(self.current_sprite_list[self.current_sprite_list_index])

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
        self.set_state(json_data["state"])

    def load_images(self):
        pass

    def event(self):
        if self.state != self.old_state:
            return self.state
        else:
            return None

    def hurt(self, severity):
        self.health -= severity
        if self.health <= 0:
            self.set_state(Entity.Dead)