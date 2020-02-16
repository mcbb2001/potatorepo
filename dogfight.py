from pygame.locals import *
import pygame
import math
import random

pygame.init()

#vars:
crashed = False
disX = 500
disY = 600
playX = disX * 0.5
playY = disY * 0.5
playdir = 15
turn = 0
speed = 2
bulSpeed = 10
score = 0
rectHeight = 30

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameFont = pygame.font.SysFont('Arial', 30)

#images
iconImg = pygame.image.load('player.90.png')
playImg = pygame.image.load('player.0.png')
tarImg = pygame.image.load('target(1).png')
bulImg = pygame.image.load('bullet.png')
iconImg = pygame.transform.scale(iconImg,(32,32))
playImg = pygame.transform.scale(playImg,(50,50))
tarImg = pygame.transform.scale(tarImg,(24,24))
bulImg = pygame.transform.scale(bulImg,(8,8))

#set display properties
pygame.display.set_icon(iconImg)
pygame.display.set_caption('Dogfight')
gameDisplay = pygame.display.set_mode((disX,disY))

#create game clock
clock = pygame.time.Clock()

class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('button.png', -1)

    def setCords(self,x,y):
        self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class Object():
    def __init__(self,playX,playY,playImg,playdir = 0):
        self.x = playX
        self.y = playY
        self.img = playImg
        self.dir = playdir
        self.get_width = self.get_rimg().get_width
        self.get_height = self.get_rimg().get_height

    def turn(self,playdir):
        self.dir += playdir

    def get_rimg(self):
        return pygame.transform.rotate(self.img, self.dir)

    def move(self,speed):
        self.x += speed*math.cos(self.dir/180*math.pi)
        self.y += speed*-math.sin(self.dir/180*math.pi)
    
    def display(self,screen):
        rimg = self.get_rimg()
        screen.blit(rimg, (int(self.x - (rimg.get_width() / 2)), int(self.y - (rimg.get_height() / 2))))

    def borderCollision(self,screen):
        return (self.x - self.get_width()/2 <= 0 or self.y - self.get_height()/2 <= rectHeight or self.x + self.get_width()/2 >= screen.get_width() or self.y + self.get_height()/2 >= screen.get_height())

    def objectCollision(self,other):
        return (other.x-other.get_width()/2 <= self.x+self.get_width()/2 and other.x+other.get_width()/2 >= self.x-self.get_width()/2 and other.y-other.get_height()/2 <= self.y+self.get_height()/2 and other.y+other.get_height()/2 >= self.y-self.get_height()/2)

class Target(Object):
    def __init__(self,tarImg,screen):
        x = (screen.get_width()-12)*random.random()+12
        y = (screen.get_height()-rectHeight-12)*random.random()+rectHeight+12
        super(Target, self).__init__(x,y,tarImg)
    
    def shot(self,screen):
        self.x = (screen.get_width()-12)*random.random()+12
        self.y = (screen.get_height()-rectHeight-12)*random.random()+rectHeight+12

class Wall(Object):
    def __init__(self,screen,x,y,width,height):
        super(Wall, self).__init__(x,y,pygame.transform.scale(bulImg,(width,height)))

class TopBar():
    def __init__(self,screen,gameFont,score):
        self.x = 0
        self.y = 0
        self.width = screen.get_width()
        self.height = rectHeight

    def display(self,screen,score):
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height))
        screen.blit(gameFont.render('Score: '+str(score),False,red),(0,0))

bullets = []

topBar = TopBar(gameDisplay,gameFont,score)
plane = Object(playX,playY,playImg)
target = Target(tarImg,gameDisplay)
wall1 = Wall(gameDisplay,150,200,10,100)
wall2 = Wall(gameDisplay,340,200,10,100)
wall3 = Wall(gameDisplay,150,400,10,100)
wall4 = Wall(gameDisplay,340,400,10,100)

pygame.key.set_repeat(100,100)

while not crashed:
    turn = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            pygame.key.get_pressed()
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                plane.turn(playdir)
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                plane.turn(-playdir)
            if pygame.key.get_pressed()[K_SPACE]:
                bullets.append(Object(plane.x,plane.y,bulImg,plane.dir))
    
    gameDisplay.fill(red)
    while target.objectCollision(wall1) or target.objectCollision(wall2) or target.objectCollision(wall3) or target.objectCollision(wall4):
        target.shot(gameDisplay)
    for bullet in bullets:
        bullet.move(bulSpeed)
        if bullet.borderCollision(gameDisplay):
            bullets.remove(bullet)
            continue
        if bullet.objectCollision(wall1) or bullet.objectCollision(wall2) or bullet.objectCollision(wall3) or bullet.objectCollision(wall4):
            bullets.remove(bullet)
            continue 
        bullet.display(gameDisplay)
        if bullet.objectCollision(target):
            bullets.remove(bullet)
            target.shot(gameDisplay)
            score += 1
            print(score)
            continue
    if plane.borderCollision(gameDisplay):
        crashed = True
    if plane.objectCollision(wall1) or plane.objectCollision(wall2) or plane.objectCollision(wall3) or plane.objectCollision(wall4):
        crashed = True

    wall1.display(gameDisplay)
    wall2.display(gameDisplay)
    wall3.display(gameDisplay)
    wall4.display(gameDisplay)
    topBar.display(gameDisplay,score)
    target.display(gameDisplay)
    plane.move(speed)
    plane.display(gameDisplay)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()