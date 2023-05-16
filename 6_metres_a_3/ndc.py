import pyxel

from background import Background
from game import Game
from player import Player
from boss import BOSS_BULLETS
from enemy import ENEMY_BULLETS
from medium_boss import MEDIUM_ENEMY_BULLETS

"""
Nuit du c0de 2023

Conçu par: Colin Cédric, Angelo Bosetti, Tony Moretti

Univers choisi: Univers 3

Nom du jeu : The Last Space Fighter
"""


# Création de la classe du Menu avec le titre et bouton start quand entrée est appuyé
class Menu:
    @staticmethod
    def draw():
        pyxel.blt(22, 30, 0, 0, 32, 84, 40)
        pyxel.text(30, 90, "Appuyez sur [ENTREE]", 1)


class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        # On initialise la ressource
        pyxel.load("3.pyxres")

        # Le statut du jeu
        # Si c'est 0, c'est le menu, et en jeu c'est 1
        self.actual_state = 0

        # On déclare le menu
        self.menu = Menu()
        # On déclare le jeu
        self.game = Game()

        # On termine en initialisant pyxel
        pyxel.run(self.update, self.draw)

    def update(self):

        # quand la touche escape est appuyée le jeu est arrêté
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.actual_state == 1:
            # Nous sommes dans le menu
            self.game.update()

        # Pour lancer le jeu
        if self.actual_state == 0 and pyxel.btn(pyxel.KEY_RETURN):
            # On met à jour le statut
            self.actual_state = 1

        # Si le joueur est mort et que la touche ENTER ou SPACE est pressée, on recommence le jeu
        if self.actual_state == 1 and self.game.player.life <= 0 and pyxel.btn(pyxel.KEY_F):
            self.game.player = Player()
            self.game.enemies = []
            self.game.medium_enemies = []
            self.game.background = Background()
            self.game.score = 0
            self.game.boss = None
            self.game.boss_timeout = self.game.BOSS_INTERVAL

            ENEMY_BULLETS.clear()
            MEDIUM_ENEMY_BULLETS.clear()
            BOSS_BULLETS.clear()

    def draw(self):
        # On nettoie l'écran
        pyxel.cls(0)
        # On dessine le menu ou le jeu
        if self.actual_state == 0:
            # Nous sommes dans le menu
            self.menu.draw()
        else:
            # Nous sommes dans le jeu
            self.game.draw()


App()
