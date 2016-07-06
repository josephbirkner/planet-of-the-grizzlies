
class SceneObject:

    box = None

    def compare(self, other):
        for dimension in [2, 1, 0]:
            if(
                (self.box.position[dimension] + self.box.size[dimension]) > other.box.position[dimension] and
                (other.box.position[dimension] + other.box.size[dimension]) > self.box.position[dimension]
            ):
                continue

            valuel = self.box.position[dimension]
            valuer = other.box.position[dimension]
            if dimension == 2:
                valuel *= -1
                valuer *= -1

            if valuel < valuer:
                return -1
            else:
                return 1

        if (-self.box.front(), self.box.top(), self.box.left()) < (-other.box.front(), other.box.top(), other.box.left()):
            return -1
        else:
            return 1

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0
