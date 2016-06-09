
from potg_entity import *


class Enemy(Entity):

    size = [139/1.5, 177/1.5, 10]

    def __init__(self, pos, world):
        super().__init__(pos, world, "gfx/stripper.png")

    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            colliding_entity.kill()

    def entity_type(self):
        return "E"