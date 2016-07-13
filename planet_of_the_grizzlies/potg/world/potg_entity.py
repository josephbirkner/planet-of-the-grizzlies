
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *
from potg_object import *

from json import *
import math

class Entity(QGraphicsPixmapItem, SceneObject):

    id = 0
    size = [0, 0, 0]
    logic_pos = [0, 0, 0]
    sprite = None
    image_offset = [0, 0]
    velocity = [0, 0, 0]
    weight = 1.0 # factor on gravity
    orientation = 1 # 1 for right, -1 for left
    jump_strength = -18
    speed = 12
    on_ground = False
    using = False
    world = None
    platform = None

    sprites = None # dictionary from the state of the entity to the its image
    sprite_cycle_timer_interval = 8  # change image every 8 updates
    current_sprite_list = None
    current_sprite_list_index = 0
    update_count = 0

    health = 100

    #state constants
    Idle = 0
    Walking = 1
    Flying = 1
    Using = 2
    Dodging = 3
    Jumping = 4
    Punching = 5
    Punched = 6
    Kicking = 7
    Kicked = 8
    Dead = 9
    Won = 10
    Captive = 11 # activated if the cage collides with the entity while being lowered
    __HighestState__ = 11

    """
    The states list is a stack of tuples. Every tuple contains
    exactly three values:
    0: The name of the state (see constants above)
    1: The maximum duration of the state (-1 if infinite)
    2: The number of updates that have passed since the state was activated
    """
    states = None
    state = None
    state_just_changed = 0

    def __init__(self, id, pos, world, filename):
        super().__init__(QPixmap(filename).scaled(self.size[0], self.size[1]), world.root)
        self.id = id
        self.world = world
        self.sprites = {}

        self.logic_pos = [pos[0], pos[1], 0]

        self.states = []
        self.velocity = [0, 0, 0]
        self.update_screen_pos()

        self.load_images()
        self.activate_state(Entity.Idle)

        self.size = self.size[0:]
        self.size[0] -= self.image_offset[0]
        self.size[1] -= self.image_offset[1]

    def killed(self):
        return self.state == Entity.Dead

    def entity_type(self):
        return "Ent"

    def update(self):
        self.update_count += 1
        self.update_count %= self.sprite_cycle_timer_interval

        if self.state_just_changed > 0:
            self.state_just_changed -= 1

        self.velocity[1] += self.world.gravity * self.weight
        self.logic_pos[0] += self.velocity[0]
        self.logic_pos[1] += self.velocity[1]
        self.logic_pos[2] += self.velocity[2]
        if self.platform and self.logic_pos[2] > self.platform.box.depth() - self.box.depth():
            self.logic_pos[2] = self.platform.box.depth() - self.box.depth()
        elif self.logic_pos[2] < 0:
            self.logic_pos[2] = 0

        if not self.platform or not self.platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
            self.update_platform()

        self.update_screen_pos()
        self.update_sprite()
        self.update_state()
        self.update_orientation()

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
                delta_y = platform.box.top() - self.box.bottom()
                if delta_y >= 0 and (delta_y < best_delta_y or best_delta_y == -1):
                    best_delta_y = delta_y
                    best_platform = platform

        if self.platform and self.platform != best_platform:
            self.platform.entities -= {self}

        self.platform = best_platform
        if self.platform:
            self.platform.entities.add(self)

    # state of the movement
    def activate_state(self, state, duration=-1, old_state=None):
        if not old_state and self.state == state:
            old_state = state

        # search state in the current states, remove if necessary
        i = 0
        for i in range(0, len(self.states)):                
            if self.states[i][0] == state:
                del self.states[i]
                break

        # put the new state on top of the states stack
        self.states.insert(0, [state, duration, 0])

        if not old_state and len(self.states) > 1:
            old_state = self.states[1][0]

        if state != old_state:
            if state in self.sprites.keys():
                self.current_sprite_list = self.sprites[state]
            else:
                print("warning: attempt to set nonexisting sprite for state",state)
                self.current_sprite_list = self.sprites[Entity.Idle]
            self.state_just_changed = 2
            self.state = state
            self.setPixmap(self.current_sprite_list[0])
            self.current_sprite_list_index = 0
            self.on_state_transition(old_state, self.state)

        self.retransform()

    def update_orientation(self):
        if self.velocity[0] < 0:
            self.orientation = -1
        else:
            self.orientation = 1

    def retransform(self):
        self.resetTransform()
        current_transform = self.transform()
        if self.orientation < 0:
            current_transform.scale(-1, 1)
            current_transform.translate(-self.boundingRect().width(), 0)
        current_transform.translate(-self.image_offset[0], -self.image_offset[1])
        self.setTransform(current_transform)

    def deactivate_state(self, state):
        i = 0
        while i < len(self.states):
            if self.states[i][0] == state:
                del self.states[i]
                if i == 0:
                    if i < len(self.states):
                        self.activate_state(self.states[i][0],
                                            self.states[i][1] - self.states[i][2] if self.states[i][1] > 0 else -1,
                                            state)
                    else:
                        print("warning: transitioning to null state!")
                break
            else:
                i += 1

    def update_state(self):
        i = 0
        while i < len(self.states):
            self.states[i][2] += 1
            if self.states[i][2] > self.states[i][1] and self.states[i][1] > 0:         # if number of updates bigger than max age of this state
                old_state = self.states[i][0]                                           # then this state becomes old_state
                del self.states[i]                                                      # delete from stack
                if i == 0:                                                              #  if top of stack
                    if i < len(self.states):                                            # if more than one state on stack
                        self.activate_state(self.states[i][0], self.states[i][1] - self.states[i][2] if self.states[i][1] > 0 else -1, old_state)       # activate state on top of stack
                    else:
                        print("warning: transitioning to null state!")
            else:
                i += 1

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
        result["state"] = [state[0:] for state in self.states]
        return result

    def deserialize(self, json_data):
        assert json_data["id"] == self.id and json_data["type"] == self.entity_type()
        self.logic_pos = json_data["pos"]
        self.velocity = json_data["velocity"]
        if not self.platform or not self.platform.box.intersectsVerticalRay(self.logic_pos[0], self.logic_pos[2]):
            self.update_platform()
        self.update_screen_pos()
        self.states = json_data["state"]
        if self.states[0][0] != self.state:
            self.activate_state(self.states[0][0])
        else:
            self.retransform()

    def load_images(self):
        pass

    def event(self):
        if self.state_just_changed > 0:
            return self.state
        else:
            return None

    def hurt(self, severity):
        self.health -= severity
        if self.health <= 0:
            self.activate_state(Entity.Dead)

    def on_state_transition(self, old_state, new_state):
        pass

    def vector_to(self, pos, speed):
        result = [
            pos[0] - self.logic_pos[0],
            pos[1] - self.logic_pos[1],
            pos[2] - self.logic_pos[2]
        ]
        result_length = math.sqrt(
            result[0] * result[0] +
            result[1] * result[1] +
            result[2] * result[2]
        )
        for i in range(0, 3):
            result[i] = result[i]/result_length * speed
        return result
