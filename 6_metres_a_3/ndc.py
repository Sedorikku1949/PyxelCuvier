from random import randint, random
import pyxel
"""
Nuit du c0de 2023

Conçu par: Colin Cédric, Angelo Bosetti, Tony Moretti

Univers choisi: Univers 3

Nom du jeu : The Last Space Fighter
"""


# Classe des tirs
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


# Création de la classe du Joueur
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


# Création de la classe du Menu avec le titre et bouton start quand entrée est appuyer
class Menu:
    def draw(self):
        pyxel.blt(22, 30, 0, 0, 32, 84, 40)
        pyxel.text(30, 90, "appuyer sur entree", 1)


# Création de la classe des ennemis
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

        for bullets in self.bullets:
            bullets.draw()

    # Gère les tirs ennemis
    def fire(self):
        bullet = Bullet(self.x + 4, self.y + 8, 2, 1)
        self.bullets.append(bullet)

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


class Background:
    def __init__(self):
        self.stars = []
        self.planet = [randint(-30, 140), -60, 0]

        self.creation()

    def creation(self):
        for i in range(75):
            # On ajoute des étoiles aléatoirement
            # Chaque étoile a pour forme [x, y]
            self.stars.append([randint(0, 128), randint(0, 128)])

    def update(self):
        # On déplace chaque étoile sur y
        for star in self.stars:
            star[1] += 0.5

        if not (self.planet is None):
            self.planet[1] += 0.40
        
        if self.planet[1] > 144:
            self.planet[0] = randint(-30, 140)
            self.planet[1] = -60
            self.planet[2] = randint(0, 1)

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
            else:
                pyxel.blt(self.planet[0], self.planet[1], 0, 200, 0, 15, 15)


class Game:
    """
    Cette class représente le jeu
    """
    def __init__(self):
        self.player = Player()

        self.background = Background()

        self.enemies = [Enemy(0, 20, 1)]

        self.score = 0

        # On stocke le nombre de temps pendant lequel aucun enemie n'est apparu
        self.since_last_enemy_spawn = 0
        

    def spawn_enemies(self):
        """
        Fait apparaitre des enemies
        """
        if random() < 0.02 or self.since_last_enemy_spawn > 30: # 2% de chance ou si aucun enemy n'est apparu pendant 1s
            if random() >= 0.5:
                # Apparait sur l'axe y à 0
                self.enemies.append(Enemy(randint(0, 75), 0, 1))
            else:
                # Apparait sur l'axe x à 0
                self.enemies.append(Enemy(0, randint(0, 75), 1))
            self.since_last_enemy_spawn = 0

            self.since_last_enemy_spawn += 1
    
    def draw(self):
        # Si la vie du joueur est à 0, on dit "game over"
        if self.player.life <= 0:
            pyxel.text(45, 62, "GAME OVER", 7)
            pyxel.text(30, 90, "Appuyez sur [ENTER]", 7)
            pyxel.text(35, 100, "pour recommencer", 7)
            
            return

        # On dessine le fond
        self.background.draw()

        # On dessine les enemies
        for enemy in self.enemies:
            enemy.draw()

        # On dessine le joueur en dernier
        self.player.draw()

        # On dessine la vie du joueur
        self.draw_life()

        # On dessine le score
        pyxel.text(10, 10, f"Score: {self.score}", 7)
        
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

        # On met à jour le Background
        self.background.update()

        # On met à jour les enemis
        for enemy in self.enemies:
            enemy.update(self.player)

        # On vérifie les balles et les enemis
        self.bullets_kills()

        self.check_enemies()

        # Apparaitre les enemies
        self.spawn_enemies()

    def bullets_kills(self):
        """
        Cette fonction permet de détruire les enemis si une balle du joueur les touches
        """
        for bullet in self.player.bullets:

            for enemy in self.enemies:
                if (enemy.x <= bullet.x <=
                        enemy.x + 9) and (enemy.y <= bullet.y <= enemy.y + 7):
                    # La balle a touchée l'enemi
                    # On le supprime
                    self.enemies.remove(enemy)
                    self.score += 1

    def check_enemies(self):
        """
        Cette fonction vérifie si un enemie a atteint le fond OU si il a touché le joueur
        Elle vérifie également si une balle d'un enemie a touché le joueur
        """

        enemies_to_remove = []

        for enemy in self.enemies:
            if enemy.y > 138:
                # Il est en dehors!
                enemies_to_remove.append(enemy)
                self.player.life -= 1

            if (enemy.y <= self.player.y <=
                    enemy.y + 9) and (enemy.x <= self.player.x <= enemy.x + 7):
                # Un enemi a touché le joueur
                self.player.life -= 1

            bullets_to_remove = []

            # On vérifie les balles
            for bullet in enemy.bullets:
                if (self.player.x <= bullet.x <= self.player.x + 9) and (
                        self.player.y <= bullet.y <= self.player.y + 7):
                    self.player.life -= 1
                    bullets_to_remove.append(bullet)

            # On retire ces balles
            for bullet in bullets_to_remove:
                enemy.bullets.remove(bullet)


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
        #quand la touche escape est appuyer le jeu est arreter 
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
        if self.actual_state == 1 and self.game.player.life <= 0 and (pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.KEY_SPACE)):
            self.game.player = Player()
            self.game.enemies = []
            self.game.background = Background()
            self.game.score = 0
            
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
