
from potg_entity import *
from potg_functions import sgn


class Enemy(Entity):

    size = [139/2.5, 177/2.5, 10]                        #two dimensional image but depth of 10

    def __init__(self, id, pos, world, image):
        super().__init__(id, pos, world, image)

    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":        #if collide with player, kill player
            colliding_entity.kill()

    def entity_type(self):
        return "E"


class PatrollingEnemy(Enemy):

    speed = 6
    direction = 0

    def __init__(self, id, pos, world, direction):
        super().__init__(id, pos, world, "gfx/ninja.png")
        self.direction = direction
        self.velocity[direction] = self.speed

    def update(self):
        if self.platform:
            self_pos = self.box.position[self.direction]
            platform_pos = self.platform.box.position[self.direction]

            distances = [
                self_pos - platform_pos,
                platform_pos + self.platform.box.size[self.direction] - self_pos - self.box.size[self.direction]
            ]

            if distances[1-sgn(self.velocity[self.direction])] < abs(self.velocity[self.direction]):
                self.velocity[self.direction] *= -1

        super().update()

    def entity_type(self):
        return "F"


class ShootingEnemy(PatrollingEnemy):

    speed = 6
    direction = 0
    shots = 3

    def __init__(self):
        super().__init__(id, pos, world, "gfx/soldat.png")

    def shoot(self):
        pass

    def update(self):
        super().update()

        while self.pos.x == player.logic_pos[0]:
            shoot()

    def entity_type(self):
        return "S"


class boss(ShootingEnemy, PatrollingEnemy):

    health = 100
    alive = True

    def __init__(self):
        super().__init__(id, pos, world, "gfx/doktor.png")

    def entity_type(self):
        return "B"