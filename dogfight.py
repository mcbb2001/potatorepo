from pygame import *
import pygame

pygame.init()

#vars:
crashed = False
disX = 400
disY = 600
playX = disX * 0.5
playY = disY * 0.5

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

def player(playX,playY):
    gameDisplay.blit(playImg, (playX,playY))

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    gameDisplay.fill(red)
        
    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()