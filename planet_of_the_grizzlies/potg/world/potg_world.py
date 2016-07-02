
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import math
import json

from potg_platforms import *
from potg_player import *
from potg_enemy import *


class World(QGraphicsScene):

    name = ""
    platforms = []
    entities = {}

    grid = []
    grid_cell_size = (10, 10)

    players = None
    spawnlocation = None

    gravity = .8
    depth_vec = (0, 0)
    depth = 0
    root = None
    update_timer_id = 0
    block_size = (41, 40)
    margin = 0
    background_image = None

    # signals
    signalPlayerPosChanged = pyqtSignal(str, QPointF)
    signalPlayerStatusChanged = pyqtSignal(str, int)

    def __init__(self, level, depth_vec=[122, 72], depth=10):
        super().__init__()
        self.name = level
        self.players = {}
        self.platforms = []
        self.entities = {}
        self.grid = []

        # normalize depth vector
        self.depth = math.sqrt(depth_vec[0]*depth_vec[0] + depth_vec[1]*depth_vec[1]) # *float(self.block_size[0)
        self.depth_vec = depth_vec
        self.block_size = (self.block_size[0], self.block_size[1])

        self.root = QGraphicsRectItem()
        self.root.setPen(QPen(Qt.NoPen))
        self.root.setPos(0, 0)
        self.addItem(self.root)

        self.width = len(level[0])
        self.height = len(level)

        # level
        level_json = open("levels/"+level+".txt").read()
        level_json = json.loads(level_json)

        self.margin = level_json["margin"]
        pos = [0, self.margin, 0]

        for line in level_json["level"]:
            pos[0] = self.margin
            last = None

            for block in line:
                next_entity_id = len(self.entities)

                if last and block == last.item_type():
                    last.width_blocks += 1
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
                        self.spawnlocation = pos[0:]
                        last = None
                    #elif block == "E":
                    #    self.entities.append(Enemy(pos[0:], self))
                    #    last = None
                    elif block == "F":
                        self.entities[next_entity_id] = PatrollingEnemy(next_entity_id, pos[0:], self, 0)
                        last = None
                    elif block == "H":
                        self.entities[next_entity_id] = PatrollingEnemy(next_entity_id, pos[0:], self, 2)
                        self.entities[next_entity_id].velocity[2] = 2
                        last = None
                    else:
                        last = None

                pos[0] += self.block_size[0]
            pos[1] += self.block_size[1]

        # background gradient
        children_rect = self.root.childrenBoundingRect()
        self.root.setRect(QRectF(0, 0, children_rect.width() + self.margin*2, children_rect.height() + self.margin*2))
        background_gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.root.rect().height()))
        background_gradient.setColorAt(0, QColor(level_json["background-gradient"][0][0], level_json["background-gradient"][0][1], level_json["background-gradient"][0][2])),
        background_gradient.setColorAt(1, QColor(level_json["background-gradient"][1][0], level_json["background-gradient"][1][1], level_json["background-gradient"][1][2]))
        self.root.setBrush(QBrush(background_gradient))

        # background image
        self.background_image = QGraphicsPixmapItem(QPixmap(level_json["background"]).scaled(
            level_json["background-size"][0],
            level_json["background-size"][1],
        ), self.root)
        self.addItem(self.background_image)
        self.background_image.setZValue(-1)

        # sort platforms by distance from camera
        self.platforms.sort(key=lambda block: (block.logic_pos[1], block.logic_pos[0]), reverse=True)
        for z in range(0, len(self.platforms)):
            self.platforms[z].setZValue(z)

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
            while True:
                next_border = (x+1) * self.grid_cell_size[0]
                if platform.box.right() > next_border:
                    x += 1
                    self.insert_into_grid(x, y, platform)
                else:
                    break

            # if the platform is wider than the grid cell, add it to the neighbouring too!
            while True:
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
        while True:
            next_border = (x + 1) * self.grid_cell_size[0]
            if box.right() > next_border:
                x += 1
                if y < len(self.grid) and x < len(self.grid[0]):
                    result += self.grid[y][x]
            else:
                break

        # if the platform is wider than the grid cell, add it to the neighbouring too!
        while True:
            next_border = (y + 1) * self.grid_cell_size[1]
            if box.bottom() > next_border:
                y += 1
                if y < len(self.grid) and x < len(self.grid[0]):
                    result += self.grid[y][x]
            else:
                break

        return result

    def entities_and_players(self):
        return list(self.entities.items())+list(self.players.items())

    def timerEvent(self, e):
        # update all entities
        for entid, ent in self.entities.items():
            ent.update()

        # update players
        for clientid, player in self.players.items():
            player.update()

        # check collision between player and entities
        for entid, ent in self.entities.items():
            for clientid, player in self.players.items():
                player.check_collision(ent)

        # check collision between entities and blocks
        for entid, ent in self.entities_and_players():
            for block in self.platforms_for_box(ent.box):
                ent.check_collision(block)

        self.update_entity_zorder()
        for clientid, player in self.players.items():
            self.signalPlayerPosChanged.emit(clientid, player.pos())

    def update_entity_zorder(self):
        for entid, ent in self.entities_and_players():
            for block in self.platforms:
                if (ent.logic_pos[1], ent.logic_pos[0]) > (block.logic_pos[1], block.logic_pos[0]):
                    ent.setZValue(block.zValue()-.5)
                    break

    def stop_updates(self):
        self.killTimer(self.update_timer_id)

    # these are used for sever-client interaction

    def add_player(self, clientid):
        self.players[clientid] = Player(self.spawnlocation[0:], self, clientid)
        return self.players[clientid]

    def player_for_client(self, clientid):
        if clientid in self.players.keys():
            return self.players[clientid]
        else:
            return None

    def changed_entities(self):
        result = []
        for entityid, entity in self.entities.items():
            result.append(entity.serialize())
        for clientid, player in self.players.items():
            result.append(player.serialize())
        return result

    def reset_changed_entities(self):
        pass

    def update_entities_from_list(self, entity_json_objects):
        for entity_info in entity_json_objects:
            if entity_info["type"] != "P":
                self.entities[entity_info["id"]].deserialize(entity_info)
            else:
                # create player if it doesnt exist yet
                player = None
                if entity_info["clientid"] in self.players.keys():
                    player = self.players[entity_info["clientid"]]
                else:
                    player = self.add_player(entity_info["clientid"])
                player.deserialize(entity_info)

    # scrolling of the background
    def scroll_background(self, player):

        # difference
        background_dx = self.root.rect().width() - self.background_image.boundingRect().width()
        background_dy = self.root.rect().height() - self.background_image.boundingRect().height()

        # proportion
        self.background_image.setPos(
            player.logic_pos[0] / self.root.rect().width() * background_dx,
            player.logic_pos[1] / self.root.rect().height() * background_dy
        )