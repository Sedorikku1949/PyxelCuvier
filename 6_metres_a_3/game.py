import pyxel
from random import randint, random

from background import Background
from enemy import ENEMY_BULLETS, Enemy
from medium_boss import MEDIUM_ENEMY_BULLETS, MediumEnemy
from player import Player
from boss import Boss, BOSS_BULLETS


class Game:
    """
    Cette class représente le jeu
    """

    def __init__(self):
        self.player = Player()

        self.background = Background()

        self.enemies = [Enemy(0, 20, 1)]
        self.medium_enemies = []

        self.score = 0

        # On stocke le nombre de temps pendant lequel aucun enemies n'est apparu
        self.since_last_enemy_spawn = 0
        self.since_last_medium_enemy_spawn = 0

        self.boss = None
        # TODO
        self.BOSS_INTERVAL = 30 * 30
        self.boss_timeout = self.BOSS_INTERVAL

    def spawn_enemies(self):
        """
        Fait apparaitre des enemies
        """
        if (self.boss is None) and random() < 0.02 or self.since_last_enemy_spawn > 120:  # 2% de chance ou si aucun
            # enemy n'est apparu pendant 1s
            self.enemies.append(Enemy(randint(0, 128), -10, 1))
            self.since_last_enemy_spawn = 0
        elif self.boss is None:
            self.since_last_enemy_spawn += 1

        if (self.boss is None) and random() < 0.005 or self.since_last_medium_enemy_spawn > 240:  # 0.5% de chance ou
            # si aucun ennemi n'est apparu pendant 4s
            self.medium_enemies.append(MediumEnemy(-10, randint(0, 25), 1))
        elif self.boss is None:
            self.since_last_enemy_spawn += 1

    def spawn_boss(self):
        """
        Fait apparaitre un boss
        """
        if not (self.boss is None):
            return

        if self.boss_timeout < 1:
            self.boss = Boss(64, -10, 0.5, 2)
            self.boss_timeout = self.BOSS_INTERVAL
        else:
            self.boss_timeout -= 1

    def boss_killed(self):
        """
        Cette fonction est appelée quand le boss meurt
        """
        self.boss = None

        self.player.life = self.player.MAX_LIFE

        self.score += 100

    def draw(self):
        # Si la vie du joueur est à 0, on dit "game over"
        if self.player.life <= 0:

            score_text = str(self.score)

            pyxel.text(47 - ((len(score_text) - 1) * 3), 20, f"Score: {score_text}", 7)
            pyxel.text(45, 62, "GAME OVER", 7)
            pyxel.text(35, 90, "Appuyez sur [F]", 7)
            pyxel.text(35, 100, "pour recommencer", 7)

            return

        # On dessine le fond
        self.background.draw()

        # On dessine les enemies
        for enemy in self.enemies:
            enemy.draw()

        for enemy in self.medium_enemies:
            enemy.draw()

        if not (self.boss is None):
            self.boss.draw()

        self.draw_bullets()

        # On dessine le joueur en dernier
        self.player.draw()

        # On dessine la vie du joueur
        self.draw_life()

        # On dessine le score
        pyxel.text(10, 10, f"Score: {self.score}", 7)

        # Alerte de boss
        if self.boss_timeout <= 30 * 4:  # 4s avant :
            pyxel.text(30, 64, "Boss en approche !!", 7)

    @staticmethod
    def draw_bullets():
        """
        Cette fonction permet de dessiner toutes les balles enemies
        """
        for bullet in ENEMY_BULLETS:
            bullet.draw()

        for bullet in MEDIUM_ENEMY_BULLETS:
            bullet.draw()

        for bullet in BOSS_BULLETS:
            bullet.draw()

    def draw_life(self):
        """
        Cette fonction dessine la vie du joueur
        """
        for i in range(0, self.player.life):
            pyxel.blt(10 + (5 + 6) * i, 113, 0, 0, 19, 7, 5, colkey=0)

    def update(self):
        # Si le joueur est mort, on stop l'update
        if self.player.life <= 0:
            return

        # on met à jour le joueur
        self.player.update()

        self.spawn_boss()

        # On met à jour le Background
        self.background.update()

        # On met à jour les enemies
        for enemy in self.enemies:
            enemy.update(self.player)

        for enemy in self.medium_enemies:
            enemy.update(self.player)

        if not (self.boss is None):
            self.boss.update(self.player)

        # On vérifie les balles et les enemies
        self.bullets_kills()
        self.update_bullets()
        self.check_enemies()

        # Apparaitre les enemies
        self.spawn_enemies()

    @staticmethod
    def update_bullets():
        """
        Cette fonction met à jour les balles
        """
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

        medium_bullets_to_remove = []
        for i in range(0, len(MEDIUM_ENEMY_BULLETS)):
            bullet = MEDIUM_ENEMY_BULLETS[i]
            if not (0 <= bullet.y <= 128):
                medium_bullets_to_remove.append(i)
            else:
                bullet.update()

        # On nettoie
        for i in range(0, len(medium_bullets_to_remove)):
            MEDIUM_ENEMY_BULLETS.pop(medium_bullets_to_remove[i] - i)

        boss_bullets_to_remove = []

        for i in range(0, len(BOSS_BULLETS)):
            bullet = BOSS_BULLETS[i]
            if not (0 <= bullet.y <= 128):
                boss_bullets_to_remove.append(i)
            else:
                bullet.update()

        # On nettoie
        for i in range(0, len(boss_bullets_to_remove)):
            BOSS_BULLETS.pop(boss_bullets_to_remove[i] - i)

    def bullets_kills(self):
        """
        Cette fonction permet de détruire les enemies si une balle du joueur les touches
        """
        bullets_to_remove = []

        for i in range(0, len(self.player.bullets)):
            bullet = self.player.bullets[i]

            for enemy in self.enemies:
                if (enemy.x <= bullet.x <= enemy.x + 9) and (enemy.y <= bullet.y <= enemy.y + 7):
                    # La balle a touché l'ennemi
                    # On le supprime
                    self.enemies.remove(enemy)
                    self.score += 1
                    bullets_to_remove.append(i)

            for enemy in self.medium_enemies:
                if (enemy.x <= bullet.x <= enemy.x + 9) and (enemy.y <= bullet.y <= enemy.y + 7):
                    # La balle a touché l'ennemi
                    enemy.life -= 1
                    if enemy.life < 1:
                        self.medium_enemies.remove(enemy)
                        self.score += 5
                    bullets_to_remove.append(i)

            if not (self.boss is None) and (self.boss.x <= bullet.x <= self.boss.x + 47) and (
                    self.boss.y <= bullet.y <= self.boss.y + 43):
                self.boss.life -= 1
                if self.boss.life < 1:
                    self.boss_killed()

        # On retire ces balles
        for bullet in bullets_to_remove:
            self.player.bullets.pop(bullet)

    def check_enemies(self):
        """
        Cette fonction vérifie si un enemies a atteint le fond OU s'il a touché le joueur.
        Elle vérifie également si une balle d'un enemies a touché le joueur
        """

        enemies_to_remove = []

        for enemy in self.enemies:
            if enemy.y > 138:
                # Il est en dehors !
                enemies_to_remove.append(enemy)
                self.player.life -= 1

            if (enemy.y <= self.player.y <= enemy.y + 9) and (enemy.x <= self.player.x <= enemy.x + 7):
                # Un ennemi a touché le joueur
                self.player.life -= 1

        medium_enemies_to_remove = []

        for enemy in self.medium_enemies:
            if enemy.y > 138:
                # Il est en dehors !
                medium_enemies_to_remove.append(enemy)
                self.player.life -= 1

            if (enemy.y <= self.player.y <= enemy.y + 9) and (enemy.x <= self.player.x <= enemy.x + 7):
                # Un ennemi a touché le joueur
                self.player.life -= 1

        # On retire ces balles
        for bullet in medium_enemies_to_remove:
            self.medium_enemies.remove(bullet)

        # On vérifie les balles
        bullets_to_remove = []

        for bullet in ENEMY_BULLETS:
            if (self.player.x <= bullet.x <= self.player.x + 9) and (
                    self.player.y <= bullet.y <= self.player.y + 7):
                self.player.life -= 1
                bullets_to_remove.append(bullet)

        # On retire ces balles
        for bullet in bullets_to_remove:
            ENEMY_BULLETS.remove(bullet)

        medium_bullets_to_remove = []
        for bullet in MEDIUM_ENEMY_BULLETS:
            if (self.player.x <= bullet.x <= self.player.x + 9) and (
                    self.player.y <= bullet.y <= self.player.y + 7):
                self.player.life -= 1
                medium_bullets_to_remove.append(bullet)

        # On retire ces balles
        for bullet in medium_bullets_to_remove:
            MEDIUM_ENEMY_BULLETS.remove(bullet)

        # On vérifie les balles
        boss_bullets_to_remove = []

        for bullet in BOSS_BULLETS:
            if (self.player.x <= bullet.x <= self.player.x + 9) and (
                    self.player.y <= bullet.y <= self.player.y + 7):
                self.player.life -= 1
                boss_bullets_to_remove.append(bullet)

        # On retire ces balles
        for bullet in boss_bullets_to_remove:
            BOSS_BULLETS.remove(bullet)
