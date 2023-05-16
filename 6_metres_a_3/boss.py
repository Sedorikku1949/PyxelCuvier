import pyxel
import math

from player import Player


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
