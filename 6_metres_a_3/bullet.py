
# Classe des tirs
import pyxel


class Bullet:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        # La direction est soit 1, soit -1
        # -1 -> Monte
        # +1 -> descend
        self.direction = direction

    def update(self):
        self.y += self.speed * self.direction

    def draw(self):
        """
        Cette fonction dessine la balle
        """
        pyxel.pset(self.x, self.y, 10)

    def __repr__(self):
        return f"Bullet({self.x}, {self.y})"