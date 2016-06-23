
import doctest

class Box:
    """
    >>> box_a = Box([1,2,3],[4,5,6])
    >>> box_b = Box([1,2,3],[4,5,6])
    >>> box_a.intersects(box_b)
    True
    >>> box_a.position[0] += 4
    >>> box_a.intersects(box_b)
    False
    """

    position = None
    size = None

    def __init__(self, position=[0, 0, 0], size=[0, 0, 0]):
        self.position = position[0:]        #copy
        self.size = size[0:]                #copy

    def setWidth(self, width):
        self.size[0] = width

    def setHeight(self, height):
        self.size[1] = height

    def setDepth(self, depth):
        self.size[2] = depth

    def width(self):
        return self.size[0]

    def height(self):
        return self.size[1]

    def depth(self):
        return self.size[2]

    # intersection
    def intersects(self, other):
        return (
            self.right() > other.left() and self.left() < other.right()
            and self.bottom() > other.top() and self.top() < other.bottom()
            and self.front() > other.back() and self.back() < other.front()
        )

    def intersectsVerticalRay(self, rx, rz):
        return (
            rx <= self.right() and rx >= self.left()
            and rz <= self.front() and rz >= self.back()
        )

    def right(self):
        return self.position[0] + self.size[0]

    def left(self):
        return self.position[0]

    def bottom(self):
        return self.position[1] + self.size[1]

    def top(self):
        return self.position[1]

    def front(self):
        return self.position[2] + self.size[2]

    def back(self):
        return self.position[2]


if __name__ == '__main__':
    doctest.testmod()