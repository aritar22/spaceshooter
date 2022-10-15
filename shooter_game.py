#Create your own shooter
from random import *
from pygame import *

window = display.set_mode((700,500))
display.set_caption("Game")

clock= time.Clock()
FPS=60

background = transform.scale(image.load("galaxy.jpg"),(700,500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image =  transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 100)
Lose = font2.render("You Lose", 5, (255,255,255))
Win = font2.render("You Win", 5, (255,255,255))
lost = 0
score = 0
lives = 3


bullet_c=0
r = False

YL = font1.render("RELOADING PLEASE WAIT", 5, (255,255,255))
class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <635:
            self.rect.x += self.speed

    def fire(self):
        global bullet_c
        global N
        global r
        global YL
        if score>=5:
            r = False
        if lost>=10:
            r = False
        if bullet_c >= 3:
            if time.get_ticks() - N < 3000:
                r = True
            else:
                bullet_c = 0
                r = False
        else:
            bullet = Bullet("bullet.png", self.rect.x, self.rect.y,10)
            bullet_c += 1
            bullets.add(bullet)
            N= time.get_ticks()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 650:
            self.rect.x = randint(80,620)
            self.rect.y = -10
            lost=lost + 1

    def respawn(self):
        self.rect.x = randint(80,620)
        self.rect.y= -100

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 650:
            self.rect.x = randint(80,620)
            self.rect.y = -7
    def respawn(self):
        self.rect.x = randint(80,620)
        self.rect.y= -100

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y<0:
            self.kill()
            del self

    

bullets = sprite.Group()


game = True
finish = False     
Enemy_group=sprite.Group()
for i in range(5):
    Enemy_group.add(Enemy("ufo.png", randint(0, 625), 10, randint(2, 4)))

Asteroid_group=sprite.Group()
for i in range(3):
    Asteroid_group.add(Asteroid("asteroid.png", randint(0, 625), 10, randint(2, 3)))

player=Player("rocket.png", 325, 400, 5)

while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
        #event of pressing the spacebar - the sprite shoots
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                
    
    if lost >= 10:
        finish=True
        window.blit(background, (0,0))
        window.blit(Lose, (200,250))
        window.blit(text_lose, (10,20))
        window.blit(text_score, (10,50))
    if score == 10:
        finish=True
        window.blit(background, (0,0))
        window.blit(Win , (200,250))
        window.blit(text_lose, (10,20))
        window.blit(text_score, (10,50))



    if finish != True:
        window.blit(background, (0,0))
        player.update()
        player.draw()
        bullets.update()
        bullets.draw(window)
        Enemy_group.update()
        Enemy_group.draw(window)
        Asteroid_group.update()
        Asteroid_group.draw(window)
        collided_sprites=sprite.groupcollide(Enemy_group, bullets, False, True)
        for item in collided_sprites:
            item.respawn()
            score += 1

        text_lose = font1.render("Missed: " + str(lost), 1, (255,255,255))
        
        text_lives = font1.render("Lives: " + str(lives), 1, (255,255,255))

        c_sprites=sprite.spritecollide(player, Asteroid_group, False)

        if c_sprites:
            lives = lives - 1
            for item in c_sprites:
                item.respawn()
            print(lives)


        if lives <=0:
            finish=True
            window.blit(background, (0,0))
            window.blit(Lose, (200,250))
            window.blit(text_lose, (10,20))
            window.blit(text_score, (10,50))            


        text_score = font1.render("Score: " + str(score), 1, (255,255,255))

        window.blit(text_lives, (10,80))
        window.blit(text_lose, (10,20))
        window.blit(text_score, (10,50))
        if r == True:
            window.blit(YL,(200, 250))
            


    clock.tick(FPS)
    display.update()