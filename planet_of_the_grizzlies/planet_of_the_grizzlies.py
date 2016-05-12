#!/usr/local/bin/python3

import pygame
import sys
from random import randint


class Block():

    rect = pygame.Rect(0, 0, 0, 0)
    color = pygame.Color(0, 0, 0)
    world = None

    def __init__(self, rct, world, col=pygame.Color(255, 0, 0)):
        self.rect = rct
        self.color = col
        self.world = world

    def type(self):
        return "_"

    def collision(self, player):
        diff = (
            (self.rect.top - player.rect.bottom),
            (self.rect.bottom - player.rect.top),
            (self.rect.left - player.rect.right),
            (self.rect.right - player.rect.left)
        )

        if player.velocity[1] > 0 and player.velocity[1]+diff[0] >= 0:
            if self.world.gravity > 0:
                player.onground = True
            player.velocity[1] = 0
            player.rect = player.rect.move(0, diff[0])
        elif player.velocity[1] < 0 and player.velocity[1]+diff[1] <= 0:
            if self.world.gravity < 0:
                player.onground = True
            player.onground = True
            player.rect = player.rect.move(0, diff[1])
            player.velocity[1] = 0

        # if the player isn't colliding anymore, skip the horizontal check
        if not player.rect.colliderect(self.rect):
            return

        if player.velocity[0] > 0 and player.velocity[0]+diff[2] >= 0:
            player.rect = player.rect.move(diff[2], 0)
            player.velocity[0] = 0
        elif player.velocity[0] < 0 and player.velocity[0]+diff[3] <= 0:
            player.rect = player.rect.move(diff[3], 0)
            player.velocity[0] = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class Water(Block):

    def __init__(self, rct, world):
        super(Water, self).__init__(rct, world, pygame.Color(50, 100, 155))

    def collision(self, player):
        player.kill()

    def type(self):
        return "W"


class TargetBlock(Block):

    def __init__(self, rct, world):
        super(TargetBlock, self).__init__(rct, world, pygame.Color(0, 255, 0))

    def collision(self, player):
        player.win()

    def type(self):
        return "T"


class Lever(Block):

    activated = False
    sprite_on = None
    sprite_off = None
    size = (60, 85)

    def __init__(self, rct, world):
        rct = pygame.Rect(rct.left, rct.top, self.size[0], self.size[1])
        super(Lever, self).__init__(rct, world)

        self.sprite_off = pygame.image.load("lever.png").convert_alpha()
        self.sprite_off = pygame.transform.scale(self.sprite_off, self.size)
        self.sprite_on = pygame.image.load("lever2.png").convert_alpha()
        self.sprite_on = pygame.transform.scale(self.sprite_on, self.size)

    def collision(self, player):
        if player.using:
            player.using = False
            self.activated = not self.activated
            player.jump_strength = -player.jump_strength
            world.gravity = -world.gravity

    def draw(self, surf):
        if self.activated:
            screen.blit(self.sprite_on, (self.rect.left, self.rect.top))
        else:
            screen.blit(self.sprite_off, (self.rect.left, self.rect.top))

    def type(self):
        return "L"


class Player():
    size = (140, 84)
    rect = pygame.Rect(0, 0, 0, 0)
    color = pygame.Color(100, 200, 50)
    sprite = None
    status = 0
    velocity = [0, 0]
    jump_strength = -19
    speed = 4.5
    onground = False
    using = False

    def __init__(self, rct):
        size = (140, 84)
        self.rect = pygame.Rect(rct.left, rct.top, self.size[0], self.size[1])
        self.sprite = pygame.image.load("grizzlie.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, self.size)

    def check_collision(self, block):
        if self.rect.colliderect(block.rect):
            block.collision(self)

    def win(self):
        self.status = 1

    def kill(self):
        self.status = -1

    def won(self):
        return self.status == 1

    def killed(self):
        return self.status == -1

    def update(self, gravity, jump, left, right, use):

        self.velocity[1] += gravity
        if jump and self.onground:
            self.velocity[1] += self.jump_strength
            self.onground = False
        if left:
            self.velocity[0] = -self.speed
        if right:
            self.velocity[0] = self.speed
        if not left and not right:
            self.velocity[0] = 0
        self.using = use
        self.rect = self.rect.move(self.velocity[0], self.velocity[1])

    def draw(self, surf):
        #pygame.draw.rect(surf, self.color, self.rect)
        screen.blit(self.sprite, (self.rect.left, self.rect.top));


class World:
    player = None
    blocks = []
    gravity = .8
    width = 0
    height = 0

    def __init__(self, level, block_width, block_height):
        pos = [0, 0]
        self.width = len(level[0])
        self.height = len(level)
        for line in level:
            pos[0] = 0
            last = None
            for block in line:
                if last and block == last.type():
                    last.rect = pygame.Rect(last.rect.x, last.rect.y, last.rect.width+block_width, last.rect.height)
                else:
                    if block == "_":
                        self.blocks.append(Block(pygame.Rect(pos[0], pos[1], block_width, block_height), self, pygame.Color(70, 90, 120)))
                        last = self.blocks[-1]
                    elif block == "T":
                        self.blocks.append(TargetBlock(pygame.Rect(pos[0], pos[1], block_width, block_height), self))
                        last = self.blocks[-1]
                    elif block == "W":
                        self.blocks.append(Water(pygame.Rect(pos[0], pos[1], block_width, block_height), self))
                        last = self.blocks[-1]
                    elif block == "L":
                        self.blocks.append(Lever(pygame.Rect(pos[0], pos[1], block_width, block_height), self))
                        last = self.blocks[-1]
                    elif block == "P":
                        self.player = Player(pygame.Rect(pos[0], pos[1], block_width, block_height))
                        last = None
                    else:
                        last = None

                pos[0] += block_width
            pos[1] += block_height

    def update(self, jump, left, right, use):
        self.player.update(self.gravity, jump, left, right, use)
        for block in self.blocks:
            self.player.check_collision(block)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)
        self.player.draw(surf)

def draw_centered(target, image):
    offx = target.get_width()/2 - image.get_width()/2
    offy = target.get_height()/2 - image.get_height() / 2
    target.blit(image, (offx, offy))

# ------------------------ Implementation ------------------------

pygame.init()

level = [
    "______________________________________________________",
    "L                                                     ",
    "                                                      ",
    "                                                      ",
    "        _____                   ________              ",
    "            _                          _              ",
    "__          _               _          _              ",
    "            _                          _              ",
    "            _     _________            ________       ",
    "            ______                            _       ",
    "                                              _TTTTTTT",
    "                           _____              ________",
    "                                                      ",
    "____                                                  ",
    "                                                 L    ",
    "                                        _             ",
    " P                                                    ",
    "                          _                          _",
    "                     _                          _     ",
    "                                                      ",
    "_____          _           _____          _           ",
    "           ___                        ___             ",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]
block_size = (30, 40)

window = pygame.display.set_mode((len(level[0])*block_size[0], len(level)*block_size[1]))
screen = pygame.display.get_surface()
pygame.display.set_caption("pyrats")

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

world = World(level, block_size[0], block_size[1])
win_banner = pygame.image.load("win.png").convert_alpha()
l00se_banner = pygame.image.load("dead.png").convert_alpha()

game_ended = False
heartbeat = pygame.time.Clock()

while not game_ended:
    use = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_ended = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                use = True
            elif event.key == pygame.K_ESCAPE:
                game_ended = True

    pressed = pygame.key.get_pressed()
    left = pressed[pygame.K_LEFT] != 0
    right = pressed[pygame.K_RIGHT] != 0
    jump = pressed[pygame.K_SPACE] != 0

    screen.blit(background, (0, 0))

    if world.player.status == 0:
        world.update(jump, left, right, use)

    world.draw(screen)

    if world.player.status < 0:
        draw_centered(screen, l00se_banner)
    elif world.player.status > 0:
        draw_centered(screen, win_banner)

    pygame.display.update()
    heartbeat.tick(60)

pygame.display.quit()
sys.exit()
