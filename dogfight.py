from pygame import *
import pygame

pygame.init()

#vars:
crashed = False
disX = 500
disY = 600
playX = disX * 0.5
playY = disY * 0.5
playdir = 90
turn = 0

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#images
playImg = pygame.image.load('player.90.png')
tarImg = pygame.image.load('target(1).png')

gameDisplay = pygame.display.set_mode((disX,disY))
pygame.display.set_caption('Dogfight')

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
    def __init__(self,playX,playY):
        self.x = int(playX)
        self.y = int(playY)

    def turn(self,playdir):
        if(turn == 0):
            playdir = playdir + 1
        if(turn == 1):
            playdir = playdir - 1

    def move(self,playdir):
        playX = speed*(playX + math.cos(playdir))
        playY = speed*(playY + math.sin(playdir))
        self.x = int(playX)
        self.y = int(playY)

while not crashed:
    turn = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.K_LEFT:
            turn = 1
        if event.type == pygame.K_RIGHT:
            turn = 3
    gameDisplay.blit(playImg, (int(playX),int(playY)))

    gameDisplay.fill(red)
        
    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()