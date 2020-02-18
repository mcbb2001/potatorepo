from pygame.locals import *
import pygame
import math
import random
import classes
import fonts

pygame.init()

#vars:
crashed = False
screenX = 500
screenY = 600
turnRate = 15
speed = 2
bulSpeed = 10
score = 0
bestScore = 0
rectHeight = 30

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#images
iconImg = pygame.image.load('Dogfight/player.90.png')
playImg = pygame.image.load('Dogfight/player.0.png')
tarImg = pygame.image.load('Dogfight/target(1).png')
bulImg = pygame.image.load('Dogfight/bullet.png')
rubImg = pygame.image.load('Dogfight/rubble.png')
iconImg = pygame.transform.scale(iconImg,(32,32))
playImg = pygame.transform.scale(playImg,(50,50))
tarImg = pygame.transform.scale(tarImg,(24,24))
bulImg = pygame.transform.scale(bulImg,(8,8))
rubImg = pygame.transform.scale(rubImg,(50,50))

#set display properties
pygame.display.set_icon(iconImg)
pygame.display.set_caption('Dogfight')
screen = pygame.display.set_mode((screenX,screenY))

#create game clock
clock = pygame.time.Clock()


title = classes.Text(screen,screenX/2,50,fonts.arial60,'Dogfight',black)
gameOver = classes.Text(screen,screenX/2,50,fonts.arial60,'Game Over',black)

gameScore = classes.Text(screen,screenX/2,0,fonts.arial30,'Score: '+str(score),red)
endScore = classes.Text(screen,screenX/2,400,fonts.arial40,'Score: '+str(score),red)

startButton = classes.Button(screen,screenX/2,135,100,50,black,fonts.arial30,'Start',red)
helpButton = classes.Button(screen,screenX/2,200,100,50,black,fonts.arial30,'Help',red)
retryButton = classes.Button(screen,screenX/2,135,100,50,black,fonts.arial30,'Retry',red)
quitButton = classes.Button(screen,screenX/2,265,100,50,black,fonts.arial30,'Quit',red)

bullets = []

player = classes.Object(screen,screenX/2,screenY/2,playImg,90,speed)
target = classes.Target(screen,tarImg)
wall1 = classes.Wall(screen,150,175,10,100,bulImg)
wall2 = classes.Wall(screen,150,screenY-175,10,100,bulImg)
wall3 = classes.Wall(screen,screenX-150,175,10,100,bulImg)
wall4 = classes.Wall(screen,screenX-150,screenY-175,10,100,bulImg)
topBar = classes.Wall(screen,screenX/2,0,screenX,70,bulImg)
pygame.key.set_repeat(100,100)

def startScreen():
    crashed = False
    startButtonC = False
    helpButtonC = False
    screen.fill(red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == MOUSEBUTTONDOWN:
            startButtonC = startButton.clicked()
            helpButtonC = helpButton.clicked()
    title.display()
    startButton.display()
    helpButton.display()
    player.display()
    startScreenList = [crashed,startButtonC,helpButtonC]
    return startScreenList

def runScreen(score,speed):
    crashed = False
    died =  False
    screen.fill(red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                player.turn(turnRate)
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                player.turn(-turnRate)
            if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
                if speed <= 5:
                    speed += 0.5
            if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
                if speed >= 1:
                    speed -= 0.5
            if pygame.key.get_pressed()[K_SPACE]:
                playerxy = player.get_xy()
                bullet = classes.Object(screen,playerxy[0],playerxy[1],bulImg,playerxy[2],bulSpeed)
                bullets.append(bullet)
    while target.objectCollision(wall1) or target.objectCollision(wall2) or target.objectCollision(wall3) or target.objectCollision(wall4) or target.objectCollision(topBar):
        target.random()
    for bullet in bullets:
        bullet.move(bulSpeed)
        if bullet.borderCollision():
            bullets.remove(bullet)
            continue
        if bullet.objectCollision(wall1) or bullet.objectCollision(wall2) or bullet.objectCollision(wall3) or bullet.objectCollision(wall4) or bullet.objectCollision(topBar):
            bullets.remove(bullet)
            continue 
        bullet.display()
        if bullet.objectCollision(target):
            bullets.remove(bullet)
            target.random()
            score += 1
            gameScore.appendText('Score: '+str(score))
            continue
    if player.borderCollision():
        died = True
    if player.objectCollision(wall1) or player.objectCollision(wall2) or player.objectCollision(wall3) or player.objectCollision(wall4) or player.objectCollision(topBar):
        died = True
    if died:
        speed = 0
        player.death(90,rubImg)
    wall1.display()
    wall2.display()
    wall3.display()
    wall4.display()
    topBar.display()
    gameScore.display()
    target.display()
    player.move(speed)
    player.display()
    runScreenList = [crashed,score,speed,died]
    return runScreenList

def gameOver(score):
    crashed = False
    retryClicked = False
    helpClicked = False
    quitClicked = False
    gameDisplay.fill(red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if pygame.mouse.get_pressed()[0]:
            retryClicked = restartButton.clicked(gameDisplay)
            helpClicked = helpButton.clicked(gameDisplay)
            quitClicked = quitButton.clicked(gameDisplay)
    if quitClicked:
        crashed = True
    if score >= bestScore.getBestScore():
        bestScore.appendBestScore(score)
    bestScore.display(gameDisplay)
    gameOverText.display(gameDisplay)
    restartButton.display(gameDisplay)
    helpButton.display(gameDisplay)
    quitButton.display(gameDisplay)
    scoreBar.display(gameDisplay,score)
    quitScreen = [crashed,retryClicked,helpClicked]
    return quitScreen

crashed = False
stage = 0
died = False

while not crashed:
    if stage == 0:
        startScreenList = startScreen()
        crashed = startScreenList[0]
        if startScreenList[1]:
            stage = 1
            continue
    elif stage == 1:
        runScreenList = runScreen(score,speed)
        crashed = runScreenList[0]
        score = runScreenList[1]
        speed = runScreenList[2]
        died = runScreenList[3]
        if died:
            stage = 2
    elif stage == 2:
        quitScreen = gameOver(score)
        crashed = quitScreen[0]
        if quitScreen[1]:
            stage = 1
            plane = Object(playX,playY,playImg,90)
            score = 0
            speed = 2
            continue
    pygame.display.update()
    clock.tick(60)
    if died:
        pygame.time.delay(1000)
        died = False