
from potg_entity import *
from potg_world import *


class Berry(Entity):

    size = [293/4, 390/4, 20]
    speed = 3

    def __init__(self, id, pos, world):
        super().__init__(id, pos, world, "gfx/berry.png")
        self.logic_pos[2] += self.world.depth*.25

    def update(self):
        super().update()
        if self.state != Entity.Captive and self.platform:
            player = self.platform.entity_for_type("P")
            if player:
                vel = self.vector_to(player.logic_pos, self.speed)
                self.velocity[0] = vel[0]
                self.velocity[2] = vel[2]
        else:
            self.velocity[0] = 0
            self.velocity[2] = 0

    def entity_type(self):
        return "g"

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/berry.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Captive] = [QPixmap("gfx/berry.png").scaled(self.size[0], self.size[1])]


class Cage(Entity):

    size = [462/2, 3703/2, 141]
    orig_y = 0

    Down = Entity.__HighestState__ + 1
    Up = Down + 1

    def __init__(self, id, pos, world):
        self.image_offset = self.image_offset[0:]
        self.image_offset[1] = 0.87 * self.size[1]

        super().__init__(id, pos, world, "gfx/cage.png")
        self.size = self.size[0:]
        self.size[0] -= 72
        self.size[1] -= 47

        self.orig_y = pos[1]
        self.activate_state(Cage.Down)

    def update(self):
        if self.state == Cage.Up and self.logic_pos[1] <= self.orig_y:
            self.weight = 0
            self.velocity[1] = 0
        super().update()

    def entity_type(self):
        return "C"

    def load_images(self):
        self.sprites[Cage.Up] = [QPixmap("gfx/cage.png").scaled(self.size[0], self.size[1])]
        self.sprites[Cage.Idle] = [QPixmap("gfx/cage.png").scaled(self.size[0], self.size[1])]
        self.sprites[Cage.Down] = [QPixmap("gfx/cage.png").scaled(self.size[0], self.size[1])]

    def on_state_transition(self, old_state, new_state):
        if new_state == Cage.Down:
            if self.weight <= 0:
                self.weight = 1.0
            for cage_platform in self.world.platforms_for_type("c"):
                cage_platform.active = True
        elif new_state == Cage.Up:
            if self.weight >= 0:
                self.weight = -1.0
            for cage_platform in self.world.platforms_for_type("c"):
                cage_platform.active = False
                cage_platform.release_captives()


