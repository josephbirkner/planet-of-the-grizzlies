
from potg_entity import *
from potg_functions import sgn

import math

class Enemy(Entity):

    size = [300/2.5, 300/2.5, 40]

    def __init__(self, id, pos, world, image):
        super().__init__(id, pos, world, image)

    def collision(self, colliding_entity):
        if colliding_entity.entity_type() == "P":
            if colliding_entity.event() == Entity.Punching or colliding_entity.event() == Entity.Kicking:
                self.hurt(colliding_entity.punch_strength)
                if not self.killed():
                    self.activate_state(Entity.Punched, 12)

    def update_target(self):
        self.current_target = None
        # check if any of the players is within range
        for clientid, player in self.world.players.items():
            dx = abs(player.logic_pos[0] - self.logic_pos[0])
            dy = abs(player.logic_pos[1] - self.logic_pos[1])
            if dx < self.range_x and dy < self.range_y:
                self.current_target = player
                break


    def entity_type(self):
        return "E"

    def load_images(self):
        pass



class Soldier(Enemy):

    speed = 6
    direction = 0
    health = 20
    range_x = 500
    range_y = 200
    current_target = None

    Aiming = Entity.__HighestState__ + 1
    Happy = Entity.__HighestState__ + 2

    bullet_burst_count = 0
    bullet_max_burst_count = 3

    def __init__(self, id, pos, world, direction):
        super().__init__(id, pos, world, "gfx/soldier_idle.png")
        self.direction = direction
        self.activate_state(Entity.Walking)

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Walking] = [QPixmap("gfx/soldier_step1.png").scaled(self.size[0], self.size[1]),
                                        QPixmap("gfx/soldier_step2.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Jumping] = [QPixmap("gfx/soldier_idle.png").scaled(self.size[0], self.size[1])]
        # self.sprites[Entity.Punching] = [QPixmap("gfx/punch_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Punched] = [QPixmap("gfx/soldier_hit.png").scaled(self.size[0], self.size[1])]
        # self.sprites[Entity.Kicking] = [QPixmap("gfx/kick_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Kicked] = [QPixmap("gfx/soldier_hit.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dead] = [QPixmap("gfx/soldier_dead.png").scaled(self.size[0], self.size[1])]
        self.sprites[Soldier.Aiming] = [QPixmap("gfx/soldier_aim.png").scaled(self.size[0], self.size[1])]
        self.sprites[Soldier.Happy] = [QPixmap("gfx/soldier_happy.png").scaled(self.size[0], self.size[1])]

    def update(self):
        if self.state == Entity.Walking:
            self.update_target()
            if self.current_target:
                self.bullet_burst_count = 0
                self.activate_state(Soldier.Aiming, 70)
            #comment
            elif self.platform:
                self_pos = self.box.position[self.direction]
                platform_pos = self.platform.box.position[self.direction]

                ###############################
                #              |              #
                #------------<-#->------------#
                #              |              #
                ###############################

                distances = [
                    self_pos - platform_pos,
                    platform_pos + self.platform.box.size[self.direction] - self_pos - self.box.size[self.direction]
                ]

                ###############################
                #              |              #
                #->------------#--------------#
                #              |              #
                ###############################

                if distances[1-sgn(self.velocity[self.direction])] < abs(self.velocity[self.direction]):
                    self.velocity[self.direction] *= -1

        super().update()


    def update_orientation(self):
        if self.current_target:
            if (self.current_target.logic_pos[0] - self.logic_pos[0]) < 0:
                self.orientation = -1
            else:
                self.orientation = 1
        else:
            super().update_orientation()

    def entity_type(self):
        return "F"

    #comment

    #  o  x
    #  |  |
    # /\ /\

    def on_state_transition(self, old_state, new_state):
        if new_state == Entity.Walking:
            self.update_target()
            if old_state == Soldier.Aiming and self.current_target:
                self.fire()
                if self.bullet_burst_count < self.bullet_max_burst_count:
                    self.activate_state(Soldier.Aiming, 20)
                else:
                    self.activate_state(Soldier.Happy, 70)
            else:
                self.velocity[self.direction] = self.speed
        elif new_state in {Entity.Dead, Entity.Punched, Entity.Kicked, Soldier.Aiming, Soldier.Happy}:
            self.velocity[self.direction] = 0

    def fire(self):
        self.update_orientation()
        nozzle_pos = [self.box.right(), (self.box.top() + self.box.bottom())/2, (self.box.back() + self.box.front())/2]
        if self.orientation < 0:
            nozzle_pos[0] = self.box.left()
        bullet = self.world.add_entity("b", nozzle_pos)
        bullet_velocity = bullet.vector_to(self.current_target.logic_pos, bullet.speed)

        self.bullet_burst_count += 1
        bullet.velocity = bullet_velocity


class Ninja(Enemy):

    speed = 8
    direction = 0
    health = 20
    range_x = 500
    range_y = 200
    current_target = None

    Aiming = Entity.__HighestState__ + 1
    Happy = Entity.__HighestState__ + 2

    bullet_burst_count = 0
    bullet_max_burst_count = 1

    def __init__(self, id, pos, world, direction):
        super().__init__(id, pos, world, "gfx/ninja.png")
        self.direction = direction
        self.activate_state(Entity.Walking)

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/ninja.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Walking] = [QPixmap("gfx/ninja_step.png").scaled(self.size[0], self.size[1]),
                                        QPixmap("gfx/ninja.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Jumping] = [QPixmap("gfx/ninja.png").scaled(self.size[0], self.size[1])]
        # self.sprites[Entity.Punching] = [QPixmap("gfx/punch_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Punched] = [QPixmap("gfx/ninja_hit.png").scaled(self.size[0], self.size[1])]
        # self.sprites[Entity.Kicking] = [QPixmap("gfx/kick_player.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Kicked] = [QPixmap("gfx/ninja_hit.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dead] = [QPixmap("gfx/ninja_dead.png").scaled(self.size[0], self.size[1])]
        self.sprites[Ninja.Aiming] = [QPixmap("gfx/ninja_attack.png").scaled(self.size[0], self.size[1])]
        self.sprites[Ninja.Happy] = [QPixmap("gfx/ninja.png").scaled(self.size[0], self.size[1])]

    def update(self):
        if self.state == Entity.Walking:
            self.update_target()
            if self.current_target:
                self.bullet_burst_count = 0
                self.activate_state(Ninja.Aiming, 70)
            elif self.platform:
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


    def update_orientation(self):
        if self.current_target:
            if (self.current_target.logic_pos[0] - self.logic_pos[0]) < 0:
                self.orientation = -1
            else:
                self.orientation = 1
        else:
            super().update_orientation()

    def entity_type(self):
        return "N"

    def on_state_transition(self, old_state, new_state):
        if new_state == Entity.Walking:
            self.update_target()
            if old_state == Ninja.Aiming and self.current_target:
                self.fire()
                if self.bullet_burst_count < self.bullet_max_burst_count:
                    self.activate_state(Ninja.Aiming, 20)
                else:
                    self.activate_state(Ninja.Happy, 70)
            else:
                self.velocity[self.direction] = self.speed
        elif new_state in {Entity.Dead, Entity.Punched, Entity.Kicked, Ninja.Aiming, Ninja.Happy}:
            self.velocity[self.direction] = 0

    def fire(self):
        self.update_orientation()
        nozzle_pos = [self.box.right(), (self.box.top() + self.box.bottom())/2, (self.box.back() + self.box.front())/2]
        if self.orientation < 0:
            nozzle_pos[0] = self.box.left()
        bullet = self.world.add_entity("s", nozzle_pos)
        bullet_velocity = bullet.vector_to(self.current_target.logic_pos, bullet.speed)

        self.bullet_burst_count += 1
        bullet.velocity = bullet_velocity


class DrEvil(Enemy):

    size = [328/3, 375/3, 20]
    Drinking = Entity.__HighestState__ + 3

    speed = 2.5
    direction = 0
    health = 999999999
    range_x = 300
    range_y = 200
    current_target = None

    def __init__(self, id, pos, world):
        super().__init__(id, pos, world, "gfx/doc_idle.png")
        self.logic_pos[2] += self.world.depth * .5

    def entity_type(self):
        return "D"

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/doc_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Using] = [QPixmap("gfx/doc_use.png").scaled(self.size[0], self.size[1])]
        self.sprites[DrEvil.Drinking] = [QPixmap("gfx/doc_drink.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Walking] = [QPixmap("gfx/doc_fly1.png").scaled(self.size[0], self.size[1]),
                                        QPixmap("gfx/doc_fly2.png").scaled(self.size[0], self.size[1])]

    def update(self):
        if self.state == Entity.Idle:
            self.update_target()
            if self.current_target:
                self.activate_state(Entity.Using, 70)
        if self.state == Entity.Walking:
            player = self.platform.entity_for_type("P")
            if not player:
                player = [p for cid, p in self.world.players.items()][0]
            if player:
                vel = self.vector_to(player.logic_pos, self.speed)
                self.velocity[0] = vel[0]
                self.velocity[2] = vel[2]

        super().update()

    def on_state_transition(self, old_state, new_state):
        if old_state == Entity.Using:
            self.activate_state(DrEvil.Drinking, 70)
        if old_state == DrEvil.Drinking:
            self.activate_state(DrEvil.Walking)
        if new_state == Entity.Captive:
            self.velocity[0] = 0
            self.velocity[2] = 0
            [p for cid, p in self.world.players.items()][0].activate_state(Entity.Won)


class Samurai(Enemy):

    size = [700/3, 700/3, 20]
    speed = 0
    direction = 0
    health = 50
    range_x = 500
    range_y = 200
    current_target = None

    def __init__(self, id, pos, world):
        super().__init__(id, pos, world, "gfx/samurai_idle.png")
        self.activate_state(Entity.Idle)
        self.logic_pos[2] += self.world.depth * .5

    def update(self):
        if self.state == Entity.Idle:
            self.update_target()
            if self.current_target:
                self.activate_state(Entity.Using, 70)

        super().update()

    def update_orientation(self):
        if self.current_target:
            if (self.current_target.logic_pos[0] - self.logic_pos[0]) < 0:
                self.orientation = -1
            else:
                self.orientation = 1
        else:
            super().update_orientation()

    def entity_type(self):
        return "x"

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/samurai_idle.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dead] = [QPixmap("gfx/samurai_dead.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Using] = [QPixmap("gfx/samurai_idle.png").scaled(self.size[0], self.size[1])]

    def on_state_transition(self, old_state, new_state):
        if new_state == Entity.Dead:
            [p for cid, p in self.world.players.items()][0].activate_state(Entity.Won)


class General(Enemy):

    size = [700/3, 700/3, 20]
    Shouting = Entity.__HighestState__ + 4

    speed = 0
    direction = 0
    health = 50
    range_x = 300
    range_y = 200
    current_target = None

    bullet_burst_count = 0
    bullet_max_burst_count = 1

    def __init__(self, id, pos, world):
        super().__init__(id, pos, world, "gfx/general.png")
        self.activate_state(Entity.Idle)
        self.logic_pos[2] += self.world.depth * .5

    def update(self):
        if self.state == Entity.Idle:
            self.update_target()
            if self.current_target:
                self.activate_state(General.Shouting, 40)

        super().update()

    def on_state_transition(self, old_state, new_state):
        if old_state == General.Shouting and self.current_target:
            self.fire()
        if new_state == Entity.Dead:
            [p for cid, p in self.world.players.items()][0].activate_state(Entity.Won)

    def fire(self):
        self.update_orientation()
        nozzle_pos = [self.box.right(), (self.box.top() + self.box.bottom()) / 2,
                      (self.box.back() + self.box.front()) / 2]
        if self.orientation < 0:
            nozzle_pos[0] = self.box.left()
        bullet = self.world.add_entity("z", nozzle_pos)
        bullet_velocity = bullet.vector_to(self.current_target.logic_pos, bullet.speed)

        self.bullet_burst_count += 1
        bullet.velocity = bullet_velocity

    def update_orientation(self):
        if self.current_target:
            if (self.current_target.logic_pos[0] - self.logic_pos[0]) < 0:
                self.orientation = -1
            else:
                self.orientation = 1
        else:
            super().update_orientation()

    def entity_type(self):
        return "y"

    def load_images(self):
        self.sprites[Entity.Idle] = [QPixmap("gfx/general.png").scaled(self.size[0], self.size[1])]
        self.sprites[Entity.Dead] = [QPixmap("gfx/general_dead.png").scaled(self.size[0], self.size[1])]
        self.sprites[General.Shouting] = [QPixmap("gfx/general_hit.png").scaled(self.size[0], self.size[1])]
