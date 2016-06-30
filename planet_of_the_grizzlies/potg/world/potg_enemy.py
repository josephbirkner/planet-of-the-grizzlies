
from potg_entity import *
from potg_functions import sgn


class Enemy(Entity):

    # two dimensional image but depth of 10
    size = [300/2.5, 300/2.5, 40]

    def __init__(self, id, pos, world, image):
        super().__init__(id, pos, world, image)

    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            if colliding_entity.event() == Entity.Punching:
                self.hurt(colliding_entity.punch_strength)
                if not self.killed():
                    self.activate_state(Entity.Punched, 25)

    def entity_type(self):
        return "E"

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Walking] = [QPixmap("gfx/soldier_step1.png").scaled(self.size[0], self.size[1]), QPixmap("gfx/soldier_step2.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Running] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dodging] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Jumping] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        #self.sprites[Entity.Punching] = [QPixmap("gfx/punch_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Punched] = [QPixmap("gfx/ninja.png").scaled(self.size[0], self.size[1])]
        #self.sprites[Entity.Kicking] = [QPixmap("gfx/kick_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Kicked] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dead] = [QPixmap("gfx/evil.png").scaled(self.size[0], self.size[1])]


class PatrollingEnemy(Enemy):

    speed = 6
    direction = 0
    health = 20

    def __init__(self, id, pos, world, direction):
        super().__init__(id, pos, world, "gfx/ninja.png")
        self.direction = direction
        self.activate_state(Entity.Walking)

    def update(self):
        if self.platform:
            self_pos = self.box.position[self.direction]
            platform_pos = self.platform.box.position[self.direction]

            # distances
            distances = [
                self_pos - platform_pos,
                platform_pos + self.platform.box.size[self.direction] - self_pos - self.box.size[self.direction]
            ]

            if distances[1-sgn(self.velocity[self.direction])] < abs(self.velocity[self.direction]):
                self.velocity[self.direction] *= -1

        super().update()

    def entity_type(self):
        return "F"

    def on_state_transition(self, old_state, new_state):
        if new_state == Entity.Walking:
            self.velocity[self.direction] = self.speed
        elif new_state in {Entity.Dead, Entity.Punched, Entity.Kicked}:
            self.velocity = [0, 0, 0]



class Bullet(Entity):

    # two dimensional image but depth of 10
    size = [50, 17, 10]
    damage = 10

    def __init__(self, id, pos, world, image):
        super().__init__(id, pos, world, image)

    # if collide with player, kill player
    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            colliding_entity.hurt(self.damage)

    def entity_type(self):
        return "b"


"""
class ShootingEnemy(PatrollingEnemy):

    speed = 0
    direction = 0
    shots = 3

    def __init__(self):
        super().__init__(id, pos, world, "gfx/soldat.png")

    def shoot(self):
        pass

    def update(self):
        super().update()

        while self.pos.z == player.logic_pos[2]:
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
"""