from pygame.locals import *
import pygame
import math

pygame.init()

#vars:
crashed = False
disX = 500
disY = 600
playX = disX * 0.5
playY = disY * 0.5
playdir = 10
turn = 0
speed = 5

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#images
playImg = pygame.image.load('player.90.png')
tarImg = pygame.image.load('target(1).png')
playImg = pygame.transform.scale(playImg,(50,50))

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

class Player():
    def __init__(self,playX,playY,playImg):
        self.x = int(playX)
        self.y = int(playY)
        self.speed = speed
        self.img = playImg
        self.dir = 0

    def turn(self,playdir):
        self.dir += playdir/180*math.pi

    def move(self,playdir):
        self.x = self.speed*(self.x + math.cos(self.playdir))
        self.y = self.speed*(self.y + math.sin(self.playdir))
    
    def display(self,screen):
        screen.blit(self.img, (self.x - int(self.img.get_width() / 2), self.y - int(self.img.get_height() / 2)))

plane = Player(playX,playY,playImg)

while not crashed:
    turn = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                plane.turn(playdir)
            if event.key == K_RIGHT:
                plane.turn(playdir)
    
    gameDisplay.fill(red)
    plane.display(gameDisplay)

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()