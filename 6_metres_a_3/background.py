from random import randint, random

import pyxel


def gen_rand_planet():
    return [randint(-15, 143), -60, randint(0, 2)]


class Background:
    def __init__(self):
        self.stars = []
        self.planet = gen_rand_planet()

        self.creation()

    def creation(self):
        for i in range(75):
            # On ajoute des étoiles aléatoirement
            # Chaque étoile a pour forme [x, y]
            self.stars.append([randint(0, 128), randint(0, 128)])

    def update(self):
        # On déplace chaque étoile sur y
        for star in self.stars:
            star[1] += 1.0

        if not (self.planet is None):
            self.planet[1] += 0.40
        
        if self.planet[1] > 144:
            self.planet = gen_rand_planet()

        # On génère de nouvelles étoiles
        if random() < 0.2:
            for i in range(3):
                self.stars.append([randint(0, 128), 0])

    def draw(self):
        for star in self.stars:
            pyxel.pset(star[0], star[1], 7)

        # On dessine la planête 1 si la troisieme variable est égale à 0 sinon on met un astéroide
        if not (self.planet is None):
            if self.planet[2] == 0:
                pyxel.blt(
                    self.planet[0],
                    self.planet[1],
                    0,
                    195,
                    39,
                    62,
                    62,
                )
            elif self.planet[2] == 1:
                pyxel.blt(
                    self.planet[0],
                    self.planet[1],
                    0,
                    218,
                    0,
                    37,
                    37 
                )
            else:
                pyxel.blt(
                    self.planet[0],
                    self.planet[1],
                    0,
                    200,
                    0,
                    16,
                    16
                )