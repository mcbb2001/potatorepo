from pygame.locals import *
import pygame
pygame.init()
#Fonts
arial30 = pygame.font.SysFont('Arial', 30, True)
arial60 = pygame.font.SysFont('Arial', 60, True)
arial40 = pygame.font.SysFont('Arial', 40, True)
#Images
iconImg = pygame.image.load('Dogfight/Images/player.90.png')
playImg = pygame.image.load('Dogfight/Images/player.0.png')
tarImg = pygame.image.load('Dogfight/Images/target(1).png')
bulImg = pygame.image.load('Dogfight/Images/bullet.png')
rubImg = pygame.image.load('Dogfight/Images/rubble.png')
bkgdImg = pygame.image.load('Dogfight/Images/bkgd.png')
iconImg = pygame.transform.scale(iconImg,(32,32))
playImg = pygame.transform.scale(playImg,(50,50))
tarImg = pygame.transform.scale(tarImg,(24,24))
bulImg = pygame.transform.scale(bulImg,(8,8))
rubImg = pygame.transform.scale(rubImg,(50,50))
#Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
