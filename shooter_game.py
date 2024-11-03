from pygame import *
from random import *
lost = 0
glases = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image) , (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = randint(0, 620)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


win = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg') , (700, 500))
win.blit(background, (0,0))
display.set_caption('стрелялочка')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('fire.ogg')

font.init()
font = font.SysFont('Arial', 35)
score = font.render('очки:', True, (151, 165, 204))
skip = font.render('пропущено:', True, (151, 165, 204))
winn = font.render('Ты выйграл =-)', True, (113, 129, 176))
lose = font.render('Ты проиграл ;-(', True, (113, 129, 176))
x1 = 250
y1 = 380
x2 = 250
y2 = -50
x3 = 200
y3 = 150

rocket = Player('rocket.png', x1, y1, 10, 80, 100 )
bullet = Bullet('bullet.png', x3, y3, 15, 20, 20)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1,6):
    monster = Enemy('ufo.png', randint(0, 620), y2, randint(1,6), 80, 50)
    monsters.add(monster) 

bullets.add(bullet)
clock = time.Clock()
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            rocket.fire()
    if finish != True:
        win.blit(background, (0,0))
        skip = font.render('пропущено: '+str(lost), True, (151, 165, 204))
        score = font.render('очки: ' +str(glases), True, (151, 165, 204))
        win.blit(score, (0,10))
        win.blit(skip, (0, 50))
        
        rocket.update()
        monsters.update()
        bullets.update()
        monsters.draw(win)
        bullets.draw(win)

        rocket.reset()
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for i in sprites_list:
            glases += 1
            monster = Enemy('ufo.png', randint(0, 620), y2, randint(1,6), 80, 50)
            monsters.add(monster)
        if glases >= 10:
            finish = True
            win.blit(winn, (250, 300))
        if lost >= 15:
            finish = True
            win.blit(lose, (300, 350))
    display.update()
    clock.tick(60)