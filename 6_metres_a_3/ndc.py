import math
import pyxel
from random import randint, random

"""
Nuit du c0de 2023

Conçu par: Colin Cédric, Angelo Bosetti, Tony Moretti

Univers choisi: Univers 3

Nom du jeu : The Last Space Fighter
"""


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
            # Chaque étoile à pour forme [x, y]
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

        # On dessine la planete 1 si la troisième variable est égale à 0 sinon on met un astéroide
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


class Player:
    """
    Cette class représente le joueur
    """

    def __init__(self):
        self.x = 64  # Moitié de 128
        self.y = 100  # Sera en bas avec 20 pixels d'écart avec le bas

        self.speed = 2  # Déplacements par pixel à chaque frame si en mouvement

        self.bullets = []

        # On alterne entre 0 et 1 (les deux canons)
        self.bullet_canon = 0

        self.life = 3
        self.MAX_LIFE = 4

        self.overheat = 0
        self.MAX_OVERHEAT = 100
        self.firing = True

    def draw(self):
        """
        Cette fonction dessine le joueur
        """
        pyxel.blt(self.x, self.y, 0, 0, 0, 9, 7, colkey=0)

        # On dessine les bullets
        for bullet in self.bullets:
            bullet.draw()

        # On dessine le overheat
        pyxel.rect(9, 122, 42, 4, 7)
        pyxel.rect(10, 123, 40 * self.overheat / self.MAX_OVERHEAT, 2, 8)

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

    def update(self):
        """
        Cette fonction est appelée à chaque mise à jour
        """
        self.update_bullets()
        self.move()

        if self.overheat >= self.MAX_OVERHEAT:
            self.firing = False

        # on tire une balle si la touche ENTER ou SPACE ou MOUSE_LEFT est pressé
        if self.firing and (pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(
                pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)) and self.overheat < self.MAX_OVERHEAT:
            # On calcule le x du canon:
            canon_x = self.bullet_canon * 8 + self.x
            # On tire une balle !
            self.bullets.append(Bullet(canon_x, self.y - 2, 3, -1))

            # On change de canon
            self.bullet_canon = (self.bullet_canon + 1) % 2

            # On augmente l'overheat
            self.overheat += 0.5
        elif self.overheat > 0:
            # On refroidit
            self.overheat -= 1

        if self.overheat <= 0:
            self.overheat = 0
            self.firing = True

    def move(self):
        """
        Cette fonction permet de détecter les mouvements du joueur et de le déplacer
        """
        # On déclare `move_x` et `move_y` pour préparer le joueur
        move_x, move_y = 0, 0

        if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            # On déplace sur y
            move_y -= self.speed
        elif pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            # On déplace sur y
            move_y += self.speed

        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT):
            # On déplace sur y
            move_x -= self.speed
        elif pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            # On déplace sur y
            move_x += self.speed

        # Si move_x et move_y sont nuls, on arrête là
        if move_x == move_y == 0:
            return

        # Si on a un déplacement sur les deux axes, il faut calculer l'hypoténuse
        if move_x != 0 and move_y != 0:
            hyp = pyxel.sqrt(move_x ** 2 + move_y ** 2)
            # On calcule un coefficient
            coeff = self.speed / hyp
            # On applique ce dernier
            move_x *= coeff
            move_y *= coeff

        # On déplace le joueur
        self.x += move_x
        self.y += move_y

        # On le bloque sur les côtés :
        if self.x > 119:
            self.x = 119
        if self.x < 0:
            self.x = 0
        if self.y > 121:
            self.y = 121
        if self.y < 0:
            self.y = 0


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


class BossBullet:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle

    def update(self):
        # Met à jour la position de la balle en fonction de l'angle et de la vitesse
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        # La ce sont les balles du boss
        pyxel.blt(self.x, self.y, 0, 96, 0, 5, 5, colkey=0)


BOSS_BULLETS: list[BossBullet] = []


class Boss:
    def __init__(self, x, y, speed, bullet_speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.fire_rate = 15
        self.fire_countdown = self.fire_rate

        self.max_life = 5000
        self.life = 5000

    def draw_bar(self):
        """
        Dessine les infos sur le boss
        """
        life_bar = 40

        pyxel.text(80, 5, "Vie du boss", 7)
        pyxel.rect(79, 14, life_bar + 2, 4, 1)
        pyxel.rect(80, 15, life_bar * (self.life / self.max_life), 2, 8)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 102, 0, 47, 43, colkey=0)  # largeur47 hauteur43

        self.draw_bar()

    def update(self, player: Player):
        player_x, player_y = player.x, player.y

        angle = math.atan2(player_y - self.y, player_x - self.x)

        # Calcule la nouvelle position horizontale en se rapprochant du joueur
        if self.x > player.x - (47 // 2):
            if abs(self.x - player.x) > self.speed:
                self.x -= self.speed
        elif self.x < player.x - (47 // 2):
            if abs(self.x - player.x) > self.speed:
                self.x += self.speed

        if self.y < 10:
            self.y += self.speed
        elif self.y < 10:
            self.y -= self.speed

        self.fire_countdown -= 1

        if self.fire_countdown <= 0:
            bullet = BossBullet(
                self.x + (47 // 2),
                self.y + (47 // 2),
                self.bullet_speed,
                angle
            )
            BOSS_BULLETS.append(bullet)

            self.fire_countdown = self.fire_rate

        for bullet in BOSS_BULLETS:
            bullet.update()


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
