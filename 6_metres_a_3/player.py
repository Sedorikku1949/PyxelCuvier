
# Création de la classe du Joueur
import pyxel

from bullet import Bullet


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

    def draw(self):
        """
        Cette fonction dessine le joueur
        """
        pyxel.blt(self.x, self.y, 0, 0, 0, 9, 7, colkey=0)

        # On dessine les bullets
        for bullet in self.bullets:
            bullet.draw()

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
        Cette fonction est appellée à chaque mise à jour
        """
        self.update_bullets()
        self.move()

        # on tire une balle si la touche ENTER ou SPACE ou MOUSE_LEFT est pressé
        if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(
                pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            # On calcule le x du canon:
            canon_x = self.bullet_canon * 8 + self.x
            # On tire une balle!
            self.bullets.append(Bullet(canon_x, self.y - 2, 3, -1))

            # On change de canon
            self.bullet_canon = (self.bullet_canon + 1) % 2

    def move(self):
        """
        Cette fonction permet de détecter les mouvements du joueur et de le déplacer
        """
        # On déclare `move_x`et `move_y` pour préparer le joueur
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

        # Si on a un déplacement sur les deux axes, il faut calculer l'hypothénuse
        if move_x != 0 and move_y != 0:
            hyp = pyxel.sqrt(move_x**2 + move_y**2)
            # On calcule un coefficient
            coeff = self.speed / hyp
            # On applique ce dernier
            move_x *= coeff
            move_y *= coeff

        # On déplace le joueur
        self.x += move_x
        self.y += move_y

        # On le bloque sur les cotés:
        if self.x > 119:
            self.x = 119
        if self.x < 0:
            self.x = 0
        if self.y > 121:
            self.y = 121
        if self.y < 0:
            self.y = 0