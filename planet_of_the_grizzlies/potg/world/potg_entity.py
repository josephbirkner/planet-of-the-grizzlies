
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *

from json import *

class Entity(QGraphicsPixmapItem):

    id = 0
    size = [0, 0, 0]
    logic_pos = [0, 0, 0]
    sprite = None
    velocity = [0, 0, 0]
    jump_strength = -18
    speed = 12
    on_ground = False
    using = False
    world = None
    box = None
    platform = None

    sprites = None
    sprite_cycle_timer_interval = 8  # change image every 8 updates
    current_sprite_list = None
    current_sprite_list_index = 0
    update_count = 0

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
        self.logic_pos = [pos[0], pos[1], 0]

        self.states = []
        self.velocity = [0, 0, 0]
        self.update_screen_pos()
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        # dictionary from the state of the entity to the its image
        self.sprites = {}

        self.load_images()
        self.activate_state(Entity.Idle)

    def killed(self):
        return self.state == Entity.Dead

    def entity_type(self):
        return "Ent"

    def update(self):
        self.update_count += 1
        self.update_count %= self.sprite_cycle_timer_interval

        if self.state_just_changed > 0:
            self.state_just_changed -= 1

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
    def activate_state(self, state, duration=-1, old_state=None):
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
            self.current_sprite_list = self.sprites[state]
            if not self.current_sprite_list:
                print("warning: attempt to set nonexisting sprite for state",state)
            self.state_just_changed = 2
            self.state = state
            self.setPixmap(self.sprites[state][0])
            self.current_sprite_list_index = 0
            self.on_state_transition(old_state, self.state)

        self.reorientate()

    def reorientate(self):
        self.resetTransform()
        if self.velocity[0] < 0:
            current_transform = self.transform()
            current_transform.scale(-1, 1)
            current_transform.translate(-self.boundingRect().width(), 0)
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
            if self.states[i][2] > self.states[i][1] and self.states[i][1] > 0:
                old_state = self.states[i][0]
                del self.states[i]
                if i == 0:
                    if i < len(self.states):
                        self.activate_state(self.states[i][0], self.states[i][1] - self.states[i][2] if self.states[i][1] > 0 else -1, old_state)
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
            self.reorientate()

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