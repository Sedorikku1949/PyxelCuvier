
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
        self.bullets = []

    def update(self, player: Player):

        # Calcule la nouvelle position horizontale en se rapprochant du joueur
        if self.x > player.x:
            self.x -= self.speed
        elif self.x < player.x:
            self.x += self.speed
        
        if self.y > player.y:
            self.y -= self.speed
        elif self.y < player.y:
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
        bullet = Bullet(self.x + 4, self.y + 8, 2, 1)
        # self.bullets.append(bullet)

        ENEMY_BULLETS.append(bullet)

    def update_bullets(self):
        """
        Cette fonction met à jour les balles et les suppriment
        si elles sont en dehors de l'écran
        """
        # On stocke les balles qui vont être retirées
        bullets_to_remove = []
        for i in range(0, len(self.bullets)):
            bullet = self.bullets[i]
            if not (0 <= bullet.y <= 128):
                bullets_to_remove.append(i)
            else:
                bullet.update()

        # On nettoie
        for i in range(0, len(bullets_to_remove)):
            self.bullets.pop(bullets_to_remove[i] - i)