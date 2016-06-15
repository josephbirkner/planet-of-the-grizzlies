
from potg_entity import *
from potg_functions import sgn


class Enemy(Entity):

    size = [139/1.5, 177/1.5, 10]

    def __init__(self, pos, world, image):
        super().__init__(pos, world, image)

    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            colliding_entity.kill()

    def entity_type(self):
        return "E"


class PatrollingEnemy(Entity):

    speed = 8
    direction = 0

    def __init__(self, pos, world, direction):
        super().__init__(pos, world, "gfx/bart.png")
        self.direction = direction
        self.velocity[direction] = self.speed

    def update(self):
        platform_box = self.platform.box
        distances = []
        for axis in range(0,3):
            distances.append([self.box.position[axis]-platform_box.position[axis], platform_box.position[axis]+platform_box.size[axis]-self.box.position[axis]-self.box.size[axis]])
        if distances[self.direction][1-sgn(self.velocity[self.direction])]<abs(self.velocity[self.direction]):
            self.velocity[self.direction] *= -1
        super(PatrollingEnemy,self).update()

    def entity_type(self):
        return "F"