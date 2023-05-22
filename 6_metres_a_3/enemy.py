# Création de la classe des ennemis
from random import random
import pyxel
from bullet import Bullet

from player import Player

ENEMY_BULLETS: list[Bullet] = []


class Enemy:

    # Initialisation de la classe de l'ennemi
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, player: Player):

        # Calcule la nouvelle position horizontale en se rapprochant du joueur
        if self.x > player.x:
            if abs(self.x - player.x + 4) > 10:
                self.x -= self.speed
        elif self.x < player.x:
            if abs(self.x - player.x + 4) > 10:
                self.x += self.speed

        if self.y > player.y:
            if abs(self.y - player.y + 4) > 30:
                self.y -= self.speed
        elif self.y < player.y:
            if abs(self.y - player.y + 4) > 30:
                self.y += self.speed

        # On met à jour les balles
        self.update_bullets()

        # Il tire aléatoirement
        if random() < 0.05:
            self.fire()

    # Affichage des ennemis
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 76, 11, 9, 8, colkey=0)

        # for bullets in self.bullets:
        #     bullets.draw()

    # Gère les tirs ennemis
    def fire(self):
        bullet = Bullet(self.x + 4, self.y + 8, 2, 0.75)
        # self.bullets.append(bullet)

        ENEMY_BULLETS.append(bullet)

    @staticmethod
    def update_bullets():
        """
        Cette fonction met à jour les balles et les suppriment
        si elles sont en dehors de l'écran
        """
        # On stocke les balles qui vont être retirées
        bullets_to_remove = []
        for i in range(0, len(ENEMY_BULLETS)):
            bullet = ENEMY_BULLETS[i]
            if not (0 <= bullet.y <= 128):
                bullets_to_remove.append(i)
            else:
                bullet.update()

        # On nettoie
        for i in range(0, len(bullets_to_remove)):
            ENEMY_BULLETS.pop(bullets_to_remove[i] - i)
