
import math
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Block(QGraphicsPixmapItem):

    width_blocks = 1
    height_blocks = 1
    sprite_width = 0
    sprite_height = 0
    logic_pos = (0, 0)
    rect = QRectF()
    logic_rect = QRect()
    world = None
    sprite = None
    brush = None
    tiles = []
    buffer = None

    def __init__(self, pos, world, sprite=None):
        super().__init__(world.root)
        if sprite is None:
            sprite = QPixmap("platform_wide.png")
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
        self.logic_rect = QRectF(self.logic_pos[0], self.logic_pos[1], self.width_blocks * self.world.block_size[0], self.height_blocks * self.world.block_size[1])
        # self.setRect(self.rect)

        # update tiles
        self.tiles.clear()
        for item in self.childItems():
            del item
        self.make_tiles()

    def item_type(self):
        return "_"

    def collision(self, player):
        diff = (
            (self.logic_rect.top() - player.logic_rect().bottom()),
            (self.logic_rect.bottom() - player.logic_rect().top()),
            (self.logic_rect.left() - player.logic_rect().right()),
            (self.logic_rect.right() - player.logic_rect().left())
        )

        if player.velocity[1] > 0 and player.velocity[1]+diff[0] >= -0.01:
            if self.world.gravity > 0:
                player.on_ground = True
            player.logic_pos[1] += diff[0]
            player.velocity[1] = 0
        elif player.velocity[1] < 0 and player.velocity[1]+diff[1] <= 0.01:
            if self.world.gravity < 0:
                player.on_ground = True
            player.logic_pos[1] += diff[1]
            player.velocity[1] = 0

        # if the player isn't colliding anymore, skip the horizontal check
        if not player.logic_rect().intersects(self.logic_rect):
            return
        if player.velocity[0] > 0 and player.velocity[0]+diff[2] >= -0.01:
            player.logic_pos[0] += diff[2]
            player.velocity[0] = 0
        elif player.velocity[0] < 0 and player.velocity[0]+diff[3] <= 0.01:
            player.logic_pos[0] += diff[3]
            player.velocity[0] = 0


class Water(Block):

    def __init__(self, pos, world):
        super().__init__(pos, world, QPixmap("water_wide.png"))

    def collision(self, player):
        player.kill()

    def item_type(self):
        return "W"


class TargetBlock(Block):

    def __init__(self, pos, world):
        super().__init__(pos, world, QPixmap("target_wide.png"))

    def collision(self, player):
        player.win()

    def item_type(self):
        return "T"


class Lever(Block):

    activated = False
    sprite_on = None
    sprite_off = None
    size = (60, 85)

    def __init__(self, pos, world):
        self.sprite_off = QPixmap("lever.png").scaled(self.size[0], self.size[1])
        self.sprite_on = QPixmap("lever2.png").scaled(self.size[0], self.size[1])
        super().__init__(pos, world, self.sprite_off)
        self.logic_rect.setWidth(self.size[0])
        self.logic_rect.setWidth(self.size[1])

    def collision(self, player):
        if player.using:
            player.using = False
            self.activated = not self.activated
            player.jump_strength = -player.jump_strength
            self.world.gravity = -self.world.gravity
            if self.activated:
                self.childItems()[-1].setPixmap(self.sprite_on)
            else:
                self.childItems()[-1].setPixmap(self.sprite_off)

    def item_type(self):
        return "L"


class Player(QGraphicsPixmapItem):

    size = (140, 84)
    logic_pos = [0, 0, 0]
    sprite = None
    status = 0
    velocity = [0, 0, 0]
    jump_strength = -19
    speed = 8
    on_ground = False
    using = False
    world = None

    def __init__(self, pos, world):
        super().__init__(QPixmap("grizzlie.png").scaled(self.size[0], self.size[1]), world.root)
        self.world = world
        self.logic_pos = [pos[0], pos[1], 0]
        self.update_screen_pos()
        self.setFlag(QGraphicsItem.ItemIsFocusable)

    def logic_rect(self):
        return QRectF(self.logic_pos[0] + 5, self.logic_pos[1] + 5, self.size[0] - 5, self.size[1] - 20)

    def check_collision(self, block):
        if self.logic_rect().intersects(block.logic_rect):
            block.collision(self)
        self.update_screen_pos()

    def win(self):
        self.status = 1
        self.world.signalPlayerStatusChanged.emit(self.status)

    def kill(self):
        self.status = -1
        self.world.signalPlayerStatusChanged.emit(self.status)

    def won(self):
        return self.status == 1

    def killed(self):
        return self.status == -1

    def update(self):
        self.velocity[1] += self.world.gravity
        self.logic_pos[0] += self.velocity[0]
        self.logic_pos[1] += self.velocity[1]
        self.logic_pos[2] += self.velocity[2]
        if self.logic_pos[2] > self.world.block_size[0] * self.world.depth:
            self.logic_pos[2] = self.world.block_size[0] * self.world.depth
        elif self.logic_pos[2] < 0:
            self.logic_pos[2] = 0
        self.update_screen_pos()

    def update_screen_pos(self):
        screen_pos = self.logic_pos[0:]
        screen_pos[0] += self.logic_pos[2] * self.world.depth_vec[0]
        screen_pos[1] += self.logic_pos[2] * self.world.depth_vec[1]
        self.setPos(screen_pos[0], screen_pos[1])

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Space and self.on_ground:
            self.velocity[1] += self.jump_strength
            self.on_ground = False
        elif e.key() == Qt.Key_Left:
            self.velocity[0] = -self.speed
        elif e.key() == Qt.Key_Right:
            self.velocity[0] = self.speed
        elif e.key() == Qt.Key_Up:
            self.velocity[2] = -self.speed
        elif e.key() == Qt.Key_Down:
            self.velocity[2] = self.speed
        elif e.key() == Qt.Key_E:
             self.using = True

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Left and self.velocity[0] < 0:
            self.velocity[0] = 0
        elif e.key() == Qt.Key_Right and self.velocity[0] > 0:
            self.velocity[0] = 0
        elif e.key() == Qt.Key_Up and self.velocity[2] < 0:
            self.velocity[2] = 0
        elif e.key() == Qt.Key_Down and self.velocity[2] > 0:
            self.velocity[2] = 0
        elif e.key() == Qt.Key_E:
            self.using = False

