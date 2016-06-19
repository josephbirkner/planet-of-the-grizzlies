
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import math

from potg_platforms import *
from potg_player import *
from potg_enemy import *


class World(QGraphicsScene):

    platforms = []
    entities = []

    grid = []                           # grid: only check small part of platforms for changes
    grid_cell_size = (10, 10)

    player = None
    gravity = .8
    depth_vec = (0, 0)
    depth = 0
    root = None
    update_timer_id = 0
    block_size = (41, 40)

    # signals
    signalPlayerPosChanged = pyqtSignal(QPointF)    #movement
    signalPlayerStatusChanged = pyqtSignal(int)     #win/dead

    def __init__(self, level, depth_vec=[122, 72], depth=10):
        super().__init__()
        self.platforms = []
        self.entities = []
        self.grid = []

        # normalize depth vector
        self.depth = math.sqrt(depth_vec[0]*depth_vec[0] + depth_vec[1]*depth_vec[1]) # *float(self.block_size[0)
        self.depth_vec = depth_vec
        self.block_size = (self.block_size[0], self.block_size[1])

        self.root = QGraphicsRectItem()
        self.root.setPen(QPen(Qt.NoPen))
        self.root.setPos(0, 0)
        self.addItem(self.root)

        pos = [0, 0, 0]
        self.width = len(level[0])
        self.height = len(level)

        #parsing level from file
        for line in open("levels/"+level+".txt"):                   # level als parameter im konstruktor
            pos[0] = 0
            last = None
            for block in line:                                      # block: characters in level string
                if last and block == last.item_type():
                    last.width_blocks += 1                          # last: for combining blocks to platforms
                    last.notify_blocks_changed()
                else:
                    if block == "_":
                        self.platforms.append(Platform(pos[0:], self))
                        last = self.platforms[-1]
                    elif block == "T":
                        self.platforms.append(TargetPlatform(pos[0:], self))
                        last = self.platforms[-1]
                    elif block == "W":
                        self.platforms.append(Water(pos[0:], self))
                        last = self.platforms[-1]
                    elif block == "L":
                        self.platforms.append(Lever(pos[0:], self))
                        last = self.platforms[-1]
                    elif block == "P":
                        self.player = Player(pos[0:], self)
                        last = None
                    #elif block == "E":
                    #    self.entities.append(Enemy(pos[0:], self))
                    #    last = None
                    elif block == "F":
                        self.entities.append(PatrollingEnemy(pos[0:], self, 0))
                        last = None
                    elif block == "H":
                        self.entities.append(PatrollingEnemy(pos[0:], self, 2))
                        self.entities[-1].velocity[2] = 2
                        last = None
                    else:
                        last = None

                pos[0] += self.block_size[0]
            pos[1] += self.block_size[1]

        # sort platforms by distance from camera
        self.platforms.sort(key=lambda block: (block.logic_pos[1], block.logic_pos[0]), reverse=True)
        for z in range(0, len(self.platforms)):
            self.platforms[z].setZValue(z)

        # focus on player
        self.setFocusItem(self.player)

        # convert grid cell size from blocks into pixels
        self.grid_cell_size = (self.grid_cell_size[0] * self.block_size[0], self.grid_cell_size[1] * self.block_size[1])

        self.sort_platforms_into_grid()

        # begin updates
        self.update_timer_id = self.startTimer(20)

    def insert_into_grid(self, x, y, platform):
        assert(x >= 0 and y >= 0)

        if len(self.grid) <= y:
            self.grid += [[] for i in range(len(self.grid), y+1)]

        if len(self.grid[0]) <= x:
            for line in self.grid:
                line += [[] for i in range(len(line), x+1)]

        print(x, y, len(self.grid), len(self.grid[0]))
        self.grid[y][x].append(platform)

    def sort_platforms_into_grid(self):
        for platform in self.platforms:
            x = int(platform.box.left()/self.grid_cell_size[0])
            y = int(platform.box.top()/self.grid_cell_size[1])

            self.insert_into_grid(x, y, platform)

            # if the platform is wider than the grid cell, add it to the neighbouring too!
            while(True):
                next_border = (x+1) * self.grid_cell_size[0]
                if platform.box.right() > next_border:
                    x += 1
                    self.insert_into_grid(x, y, platform)
                else:
                    break

            # if the platform is wider than the grid cell, add it to the neighbouring too!
            while (True):
                next_border = (y+1) * self.grid_cell_size[1]
                if platform.box.bottom() > next_border:
                    y += 1
                    self.insert_into_grid(x, y, platform)
                else:
                    break

    def platforms_for_box(self, box):
        result = []

        x = int(box.left() / self.grid_cell_size[0])
        y = int(box.top() / self.grid_cell_size[1])
        w = box.width()
        h = box.height()

        if y < len(self.grid) and x < len(self.grid[0]):
            result += self.grid[y][x]

        # if the platform is wider than the grid cell, add it to the neighbouring too!
        while (True):
            next_border = (x + 1) * self.grid_cell_size[0]
            if box.right() > next_border:
                x += 1
                if y < len(self.grid) and x < len(self.grid[0]):
                    result += self.grid[y][x]
            else:
                break

        # if the platform is wider than the grid cell, add it to the neighbouring too!
        while (True):
            next_border = (y + 1) * self.grid_cell_size[1]
            if box.bottom() > next_border:
                y += 1
                if y < len(self.grid) and x < len(self.grid[0]):
                    result += self.grid[y][x]
            else:
                break

        return result

    def timerEvent(self, e):
        # update all entities
        for ent in self.entities:
            ent.update()
        self.player.update()

        # check collision between player and entities
        for ent in self.entities:
            self.player.check_collision(ent)

        # check collision between entities and blocks
        for ent in self.entities+[self.player]:
            for block in self.platforms_for_box(ent.box):
                ent.check_collision(block)

        self.update_entity_zorder()
        self.signalPlayerPosChanged.emit(self.player.pos())

    def update_entity_zorder(self):
        for ent in self.entities+[self.player]:
            for block in self.platforms:
                if (ent.logic_pos[1], ent.logic_pos[0]) > (block.logic_pos[1], block.logic_pos[0]):
                    ent.setZValue(block.zValue()-.5)
                    break

    def stop_updates(self):
        self.killTimer(self.update_timer_id)
