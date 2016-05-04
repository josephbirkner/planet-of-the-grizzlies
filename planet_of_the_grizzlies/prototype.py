#!/usr/local/bin/python3

import pygame
import sys
from random import randint


class Block():
    rect = pygame.Rect(0, 0, 0, 0)
    color = pygame.Color(0, 0, 0)

    def __init__(self, rct, col):
        self.rect = rct
        self.color = col

    def collision(self, player):
        diff = (
            (self.rect.top - player.rect.bottom, player.rect.top < self.rect.top),
            (self.rect.bottom - player.rect.top, player.rect.bottom > self.rect.bottom),
            (self.rect.left - player.rect.right, player.rect.left < self.rect.left),
            (self.rect.right - player.rect.left, player.rect.right > self.rect.right)
        )
        if  ((diff[0][0] < 0 and diff[0][1]) or \
            (diff[1][0] > 0 and diff[0][1])) and \
            not (diff[0][0] < 0 and diff[1][0] > 0 and diff[0][1] and diff[1][1]):
            player.rect = player.rect.move(0, -player.velocity[1])
            player.velocity[1] /= 2

        if  ((diff[2][0] < 0 and diff[2][1]) or \
            (diff[3][0] > 0 and diff[3][1])) and \
            not (diff[2][0] < 0 and diff[3][0] > 0 and diff[2][1] and diff[3][1]):
            print(diff)
            player.rect = player.rect.move(-player.velocity[0], 0)
            player.velocity[0] /= 2

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class Water(Block):

    def __init__(self, rct):
        super(Water, self).__init__(rct, pygame.Color(50, 100, 155))

    def collision(self, player):
        player.kill()


class TargetBlock(Block):

    def __init__(self, rct):
        super(TargetBlock, self).__init__(rct, pygame.Color(255, 0, 0))

    def collision(self, player):
        player.win()


class Player():
    rect = pygame.Rect(0, 0, 0, 0)
    color = pygame.Color(100, 200, 50)
    status = 0
    velocity = [0, 0]
    jump_strength = -5
    speed = 5

    def __init__(self, rct):
        self.rect = rct

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

    def update(self, gravity, jump, left, right):

        self.velocity[1] += gravity
        if jump:
            self.velocity[1] += self.jump_strength
        if left:
            self.velocity[0] = -self.speed
        if right:
            self.velocity[0] = self.speed
        if not left and not right:
            self.velocity[0] = 0
        self.rect = self.rect.move(self.velocity[0], self.velocity[1])

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class World:
    player = None
    blocks = []
    gravity = 1

    def __init__(self, level, width, height):
        block_width = width/len(level[0])
        block_height = height/len(level)
        pos = [0, 0]
        for line in level:
            pos[0] = 0
            for block in line:
                if block == "_":
                    self.blocks.append(Block(pygame.Rect(pos[0], pos[1], block_width+1, block_height+1), pygame.Color(70, 90, 120)))
                elif block == "T":
                    self.blocks.append(TargetBlock(pygame.Rect(pos[0], pos[1], block_width+1, block_height+1)))
                elif block == "W":
                    self.blocks.append(Water(pygame.Rect(pos[0], pos[1], block_width+1, block_height+1)))
                elif block == "P":
                    self.player = Player(pygame.Rect(pos[0], pos[1], block_width+1, block_height+1))
                pos[0] += block_width
            pos[1] += block_height

    def update(self, jump, left, right):
        self.player.update(self.gravity, jump, left, right)
        for block in self.blocks:
            self.player.check_collision(block)

    def draw(self, surf):
        for block in self.blocks:
            block.draw(surf)
        self.player.draw(surf)


# ------------------------ Implementation ------------------------

pygame.init()

window = pygame.display.set_mode((640, 480))
screen = pygame.display.get_surface()
pygame.display.set_caption("pyrats")

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

heartbeat = pygame.time.Clock()
world = World(
    [
        "                           ",
        "                           ",
        "                           ",
        "              ___          ",
        "       ___                 ",
        "                           ",
        "                        TT ",
        "                  _____    ",
        "             _____         ",
        "P      ______              ",
        "_____                      ",
        "                           ",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWW"
    ],
    640,
    480
)

game_ended = False

while world.player.status == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_ended = True

    pressed = pygame.key.get_pressed()
    left = pressed[pygame.K_LEFT] != 0
    right = pressed[pygame.K_RIGHT] != 0
    jump = pressed[pygame.K_SPACE] != 0

    screen.blit(background, (0, 0))
    world.update(jump, left, right)
    world.draw(screen)
    pygame.display.update()
    heartbeat.tick(20)

pygame.display.quit()
sys.exit()
