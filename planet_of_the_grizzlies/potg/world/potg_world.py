
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import math

from potg_platforms import *
from potg_player import *
from potg_enemy import *


class World(QGraphicsScene):

    blocks = []
    entities = []
    player = None
    gravity = .8
    depth_vec = (0, 0)
    depth = 0
    root = None
    update_timer_id = 0
    block_size = (41, 40)

    # signals
    signalPlayerPosChanged = pyqtSignal(QPointF)
    signalPlayerStatusChanged = pyqtSignal(int)

    def __init__(self, level, depth_vec=[122, 72], depth=10):
        super().__init__()

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
        for line in open("levels/"+level+".txt"):
            pos[0] = 0
            last = None
            for block in line:
                if last and block == last.item_type():
                    last.width_blocks += 1
                    last.notify_blocks_changed()
                else:
                    if block == "_":
                        self.blocks.append(Platform(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "T":
                        self.blocks.append(TargetPlatform(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "W":
                        self.blocks.append(Water(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "L":
                        self.blocks.append(Lever(pos[0:], self))
                        last = self.blocks[-1]
                    elif block == "P":
                        self.player = Player(pos[0:], self)
                        last = None
                    #elif block == "E":
                    #    self.entities.append(Enemy(pos[0:], self))
                    #    last = None
                    elif block == "F":
                        self.entities.append(PatrollingEnemy(pos[0:], self, 0))
                        last = None
                    else:
                        last = None

                pos[0] += self.block_size[0]
            pos[1] += self.block_size[1]

        # sort block by distance from camera
        self.blocks.sort(key=lambda block: (block.logic_pos[1], block.logic_pos[0]), reverse=True)
        for z in range(0, len(self.blocks)):
            self.blocks[z].setZValue(z)

        self.setFocusItem(self.player)

        # begin updates
        self.update_timer_id = self.startTimer(20)

    def timerEvent(self, e):
        # update all entities
        for ent in self.entities:
            ent.update()
        self.player.update()

        # check collision between player and entities
        for ent in self.entities:
            self.player.check_collision(ent)

        # check collision between entities and blocks
        for block in self.blocks:
            self.player.check_collision(block)
            for ent in self.entities:
                ent.check_collision(block)

        self.update_entity_zorder()
        self.signalPlayerPosChanged.emit(self.player.pos())

    def update_entity_zorder(self):
        for ent in self.entities+[self.player]:
            for block in self.blocks:
                if (ent.logic_pos[1], ent.logic_pos[0]) > (block.logic_pos[1], block.logic_pos[0]):
                    ent.setZValue(block.zValue()-.5)
                    break

    def stop_updates(self):
        self.killTimer(self.update_timer_id)
