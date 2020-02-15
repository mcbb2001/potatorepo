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

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#images
playImg = pygame.image.load('player.0.png')
tarImg = pygame.image.load('target(1).png')
bulImg = pygame.image.load('bullet.png')
playImg = pygame.transform.scale(playImg,(50,50))
tarImg = pygame.transform.scale(tarImg,(24,24))
bulImg = pygame.transform.scale(bulImg,(8,8))

#set display properties
gameDisplay = pygame.display.set_mode((disX,disY))
pygame.display.set_caption('Dogfight')

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
        return (self.x - self.get_width()/2 <= 0 or self.y - self.get_height()/2 <= 0 or self.x + self.get_width()/2 >= screen.get_width() or self.y + self.get_height()/2 >= screen.get_height())

    def objectCollision(self,other):
        return (other.x-other.get_width() <= self.x and other.x+other.get_width() >= self.x and other.y-other.get_height() <= self.y and other.y+other.get_height() >= self.y)

class Target(Object):
    def __init__(self,tarImg,screen):
        x = screen.get_width()*random.random()
        y = screen.get_height()*random.random()
        super(Target, self).__init__(x,y,tarImg)




bullets = []

plane = Object(playX,playY,playImg)
target = Target(tarImg,gameDisplay)

while not crashed:
    turn = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                plane.turn(playdir)
            if event.key == K_RIGHT:
                plane.turn(-playdir)
            if event.key == K_SPACE:
                bullets.append(Object(plane.x,plane.y,bulImg,plane.dir))

    
    gameDisplay.fill(red)
    for bullet in bullets:
        bullet.move(bulSpeed)
        if bullet.borderCollision(gameDisplay):
            bullets.remove(bullet)
            continue
        bullet.display(gameDisplay)
        if bullet.objectCollision(target):
            bullets.remove(bullet)
            score += 1
            continue
    if plane.borderCollision(gameDisplay):
        crashed = True
    target.display(gameDisplay)
    plane.move(speed)
    plane.display(gameDisplay)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()