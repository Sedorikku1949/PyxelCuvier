# Nuit du c0de 2023

import pyxel



class App :
    def __init__(self) :
        pyxel.init(128, 128, title="SUPER MONKEY SMASH", fps=24)
        self.x_un = 0
        self.y_un = 96
        self.velx_un = 0
        self.vely_un = 0
        self.x_de = 112
        self.y_de = 96
        self.velx_de = 0
        self.vely_de = 0
        self.vie_un = 50
        self.vie_de = 50
        self.sprite_un = 0
        self.sprite_de = 16
        self.sprite_unS = 0
        self.sprite_deS = 16
        self.duree_c = 3
        self.victory=""
        pyxel.load("theme.pyxres")
        pyxel.run(self.update, self.draw)
        
    def update(self) :
        self.J_un()
        self.J_de()
        
    def draw(self) :
        pyxel.cls(12)
        pyxel.blt(0, 112, 0, 0,88, 128,16, 0)
        pyxel.blt(self.x_un, self.y_un, 0, self.sprite_un,self.sprite_unS, 16,16, 0)
        pyxel.blt(self.x_de, self.y_de, 0, self.sprite_de,self.sprite_deS, 16,16, 0)
        pyxel.rect(0,4, 50, 8, 7)
        pyxel.rect(78,4, 50, 8, 7)
        pyxel.rect(0,4, self.vie_un, 8, 11)
        pyxel.rect(78,4, self.vie_de, 8, 11)
        pyxel.blt(56,0,0, 0,120,16,16,0)
        pyxel.text(40,64,self.victory,0)
        
    
    def colision(self):
        if (self.x_un+16,self.y_un) == (self.x_de,self.y_de):
            return 1
        if (self.x_un,self.y_un) == (self.x_de+16,self.y_de):
            return 2
        
    def J_un(self) :
        
        if self.sprite_un==32 :
            self.duree_c-=1
            if self.duree_c==0 :
                self.duree_c=3
                self.sprite_un=0
        elif self.sprite_un==48 :
            self.duree_c-=1
            if self.duree_c==0 :
                self.duree_c=3
                self.sprite_un=16
        
        
        if self.y_un < 96 :
            self.vely_un += 1
            self.sprite_unS =32
        else:
            self.vely_un = 0
            self.sprite_unS =0
            
        if pyxel.btn(pyxel.KEY_D) and self.x_un<112 and self.colision() != 1 :
            self.sprite_un = 0
            self.x_un = (self.x_un + 3)
        elif pyxel.btn(pyxel.KEY_Q) and self.x_un>0 and self.colision() != 2 :
            self.sprite_un = 16
            self.x_un = (self.x_un - 3)
        if pyxel.btn(pyxel.KEY_Z) and self.y_un==96 :
            self.vely_un += -12
        else:
            self.velx_un = 0
        
        if pyxel.btnr(pyxel.KEY_A) and self.sprite_un==0:
            self.sprite_un = 32
            if self.x_un +16 <= self.x_de and self.x_un +32 >= self.x_de:
                self.vie_de -= 5
        elif pyxel.btnr(pyxel.KEY_A) and self.sprite_un==16:
            self.sprite_un = 48
            if self.x_un >= self.x_de and self.x_un -32 <= self.x_de:
                self.vie_de -= 5
                
        if self.vie_un <= 0:
            self.vely_un = -12
            self.velx_un = -6
            self.victory = "PLAYER 2 WON"
        
        self.x_un += self.velx_un
        self.y_un += self.vely_un
        
        
    def J_de(self) :
        if self.sprite_de==32 :
            self.duree_c-=1
            if self.duree_c==0 :
                self.duree_c=3
                self.sprite_de=0
        elif self.sprite_de==48 :
            self.duree_c-=1
            if self.duree_c==0 :
                self.duree_c=3
                self.sprite_de=16
        
        if self.y_de < 96 :
            self.vely_de += 1
            self.sprite_deS =48
        else:
            self.vely_de = 0
            self.sprite_deS =16
            
        if pyxel.btn(pyxel.KEY_KP_6) and self.x_de<112 and self.colision() != 2 :
            self.sprite_de = 0
            self.x_de = (self.x_de + 3)
        elif pyxel.btn(pyxel.KEY_KP_4) and self.x_de>0 and self.colision() != 1 :
            self.sprite_de = 16
            self.x_de = (self.x_de - 3)
        if pyxel.btn(pyxel.KEY_KP_8) and self.y_de==96 :
            self.vely_de += -12
        else:
            self.velx_de = 0
            
        if pyxel.btnr(pyxel.KEY_KP_9) and self.sprite_de==0:
            self.sprite_de = 32
            if self.x_de +16 <= self.x_de and self.x_de +32 >= self.x_un:
                self.vie_un -= 5
        elif pyxel.btnr(pyxel.KEY_KP_9) and self.sprite_de==16:
            self.sprite_de = 48
            if self.x_de >= self.x_un and self.x_de -32 <= self.x_un:
                self.vie_un -= 5
    
        if self.vie_de <= 0:
            self.vely_de = -12
            self.velx_de = 6
            self.victory = "PLAYER 1 WON"
            
        self.x_de += self.velx_de
        self.y_de += self.vely_de
    

        
App()