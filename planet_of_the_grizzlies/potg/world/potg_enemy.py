
from potg_entity import *
from potg_functions import sgn


class Enemy(Entity):

    # two dimensional image but depth of 10
    size = [139/2.5, 177/2.5, 10]

    def __init__(self, id, pos, world, image):
        super().__init__(id, pos, world, image)

    # if collide with player, kill player
    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            colliding_entity.kill()

    def entity_type(self):
        return "E"

    def load_images(self):
        self.sprites[Entity.Idle] = QPixmap("gfx/walk_enemy.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Walking] = QPixmap("gfx/walk_enemy.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Running] = QPixmap("gfx/walk_enemy.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Dodging] = QPixmap("gfx/walk_enemy.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Jumping] = QPixmap("gfx/walk_enemy.png").scaled(self.size[0], self.size[1])
        #self.sprites[Entity.Punching] = QPixmap("gfx/punch_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Punched] = QPixmap("gfx/punch_enemy.png").scaled(self.size[0], self.size[1])
        #self.sprites[Entity.Kicking] = QPixmap("gfx/kick_player.png").scaled(self.size[0], self.size[1])
        self.sprites[Entity.Kicked] = QPixmap("gfx/kick_enemy.png").scaled(self.size[0], self.size[1])


class PatrollingEnemy(Enemy):

    speed = 6
    direction = 0

    def __init__(self, id, pos, world, direction):
        super().__init__(id, pos, world, "gfx/walk_enemy.png")
        self.direction = direction
        self.velocity[direction] = self.speed

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