
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from potg_box import *


class Platform(QGraphicsPixmapItem):

    width_blocks = 1
    height_blocks = 1
    sprite_width = 0
    sprite_height = 0
    logic_pos = (0, 0)
    rect = QRectF()
    box = Box()
    world = None
    sprite = None
    brush = None
    tiles = []
    buffer = None

    def __init__(self, pos, world, sprite=None):
        super().__init__(world.root)
        if sprite is None:
            sprite = QPixmap("gfx/platform_wide.png")
        self.logic_pos = pos
        self.rect = QRectF()
        self.world = world
        self.setPos(pos[0], pos[1])
        self.setVisible(True)
        #self.setBrush(QBrush(Qt.NoBrush))
        #self.setPen(QPen(Qt.NoPen))
        self.sprite = sprite
        self.sprite_width = self.sprite.width()
        self.sprite_height = self.sprite.height()
        self.notify_blocks_changed()

    def make_tiles(self):
        self.buffer = QPixmap(self.rect.width(), self.rect.height())
        self.buffer.fill(Qt.transparent)
        painter = QPainter(self.buffer)
        for i in range(self.height_blocks, 0, -1):
            for j in range(self.width_blocks, 0, -1):
                # tile = QGraphicsPixmapItem(self.sprite, self)
                # tile.setPos(self.world.block_size[0]*(j-1), self.world.block_size[1]*(i-1))
                painter.drawPixmap(self.world.block_size[0]*(j-1), self.world.block_size[1]*(i-1), self.sprite)
        painter.end()
        self.setPixmap(self.buffer)

    def notify_blocks_changed(self):
        self.rect = QRectF(0, 0, (self.width_blocks-1)*self.world.block_size[0], (self.height_blocks-1)*self.world.block_size[1])
        self.rect.adjust(0, 0, self.sprite_width, self.sprite_height)
        self.box = Box(self.logic_pos, [self.width_blocks * self.world.block_size[0], self.height_blocks * self.world.block_size[1], self.world.depth])
        # self.setRect(self.rect)

        # update tiles
        self.tiles.clear()
        for item in self.childItems():
            del item
        self.make_tiles()

    def item_type(self):
        return "_"

    def collision(self, ent):
        diff = (
            (self.box.top() - ent.box.bottom()),
            (self.box.bottom() - ent.box.top()),
            (self.box.left() - ent.box.right()),
            (self.box.right() - ent.box.left())
        )

        if ent.velocity[1] > 0 and ent.velocity[1]+diff[0] >= -0.01:
            if self.world.gravity > 0:
                ent.on_ground = True
            ent.logic_pos[1] += diff[0]
            ent.velocity[1] = 0
        elif ent.velocity[1] < 0 and ent.velocity[1]+diff[1] <= 0.01:
            if self.world.gravity < 0:
                ent.on_ground = True
            ent.logic_pos[1] += diff[1]
            ent.velocity[1] = 0

        # if the player isn't colliding anymore, skip the horizontal check
        if not ent.box.intersects(self.box):
            return
        if ent.velocity[0] > 0 and ent.velocity[0]+diff[2] >= -0.01:
            ent.logic_pos[0] += diff[2]
            ent.velocity[0] = 0
        elif ent.velocity[0] < 0 and ent.velocity[0]+diff[3] <= 0.01:
            ent.logic_pos[0] += diff[3]
            ent.velocity[0] = 0


class Water(Platform):

    def __init__(self, pos, world):
        super().__init__(pos, world, QPixmap("gfx/water_wide.png"))

    def collision(self, ent):
        if ent.entity_type() == "P":
            ent.kill()

    def item_type(self):
        return "W"


class TargetPlatform(Platform):

    def __init__(self, pos, world):
        super().__init__(pos, world, QPixmap("gfx/target_wide.png"))

    def collision(self, ent):
        if ent.entity_type() == "P":
            ent.win()

    def item_type(self):
        return "T"


class Lever(Platform):

    activated = False
    sprite_on = None
    sprite_off = None
    size = (60, 85)

    def __init__(self, pos, world):
        self.sprite_off = QPixmap("gfx/lever.png").scaled(self.size[0], self.size[1])
        self.sprite_on = QPixmap("gfx/lever2.png").scaled(self.size[0], self.size[1])
        super().__init__(pos, world, self.sprite_off)
        self.box.setWidth(self.size[0])
        self.box.setHeight(self.size[1])

    def collision(self, ent):
        if ent.using:
            ent.using = False
            self.activated = not self.activated
            ent.jump_strength = -ent.jump_strength
            self.world.gravity = -self.world.gravity
            if self.activated:
                self.setPixmap(self.sprite_on)
            else:
                self.setPixmap(self.sprite_off)

    def item_type(self):
        return "L"
