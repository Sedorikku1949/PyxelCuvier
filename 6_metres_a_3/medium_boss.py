# Création de la classe des ennemis
from random import random
import pyxel

from player import Player


class MediumEnemyBullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        # Met à jour la position de la balle
        self.y += self.speed

    def draw(self):
        # La ce sont les balles
        pyxel.blt(self.x, self.y, 0, 64, 16, 3, 3, colkey=0)


MEDIUM_ENEMY_BULLETS: list[MediumEnemyBullet] = []


class MediumEnemy:

    # Initialisation de la classe de l'ennemi
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        self.life = 5

    def update(self, player: Player):

        # Calcule la nouvelle position horizontale en se rapprochant du joueur
        if self.x > player.x:
            if abs(self.x - player.x + 4) > 5:
                self.x -= self.speed
        elif self.x < player.x:
            if abs(self.x - player.x + 4) > 5:
                self.x += self.speed

        if self.y < 20:
            self.y += self.speed
        elif self.y < 20:
            self.y -= self.speed

        # On met à jour les balles
        self.update_bullets()

        # Il tire aléatoirement
        if random() < 0.05:
            self.fire()

    # Affichage des ennemis
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 44, 0, 15, 15, colkey=0)

    # Gère les tirs ennemis
    def fire(self):
        bullet = MediumEnemyBullet(self.x + 4, self.y + 8, 1.5)

        MEDIUM_ENEMY_BULLETS.append(bullet)

    @staticmethod
    def update_bullets():
        """
        Cette fonction met à jour les balles et les suppriment
        si elles sont en dehors de l'écran
        """
        # On stocke les balles qui vont être retirées
        bullets_to_remove = []
        for i in range(0, len(MEDIUM_ENEMY_BULLETS)):
            bullet = MEDIUM_ENEMY_BULLETS[i]
            if not (0 <= bullet.y <= 128):
                bullets_to_remove.append(i)
            else:
                bullet.update()

        # On nettoie
        for i in range(0, len(bullets_to_remove)):
            MEDIUM_ENEMY_BULLETS.pop(bullets_to_remove[i] - i)
