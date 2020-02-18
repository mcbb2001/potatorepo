from pygame.locals import *
import pygame
import time
import math
import random
import classes
import inits

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
stage = 0
storedStage = 0
died = False
helpScreenStage = 0

#set display properties
pygame.display.set_icon(inits.iconImg)
pygame.display.set_caption('Dogfight')
screen = pygame.display.set_mode((screenX,screenY))

#create game clock
clock = pygame.time.Clock()


title = classes.Text(screen,screenX/2,50,inits.arial60,'Dogfight',inits.black)
gameOver = classes.Text(screen,screenX/2,50,inits.arial60,'Game Over',inits.black)

gameScore = classes.Text(screen,screenX/2,0,inits.arial30,'Score: '+str(score),inits.red)
endScore = classes.Text(screen,screenX/2,400,inits.arial40,'Score: '+str(score),inits.red)
bestScoretxt = classes.Text(screen,screenX/2,450,inits.arial40,'Best Score: '+str(bestScore),inits.black)

startButton = classes.Button(screen,screenX/2,135,100,50,inits.black,inits.arial30,'Start',inits.red)
helpButton = classes.Button(screen,screenX/2,200,100,50,inits.black,inits.arial30,'Help',inits.red)
retryButton = classes.Button(screen,screenX/2,135,100,50,inits.black,inits.arial30,'Retry',inits.red)
quitButton = classes.Button(screen,screenX/2,265,100,50,inits.black,inits.arial30,'Quit',inits.red)
nextButton = classes.Button(screen,screenX-screenX/4,500,100,50,inits.black,inits.arial30,'Next',inits.red)
backButton = classes.Button(screen,screenX/4,500,100,50,inits.black,inits.arial30,'Back',inits.red)
exitButton = classes.Button(screen,50,10,100,50,inits.red,inits.arial30,'Exit',inits.black)

helpScreenLine1 = classes.Text(screen,screenX/2,100,inits.arial30,'helpScreenLine1',inits.black)
helpScreenLine2 = classes.Text(screen,screenX/2,140,inits.arial30,'helpScreenLine2',inits.black)
helpScreenLine3 = classes.Text(screen,screenX/2,180,inits.arial30,'helpScreenLine3',inits.black)

bullets = []

player = classes.Object(screen,screenX/2,screenY/2+60,inits.playImg,90,speed)
target = classes.Target(screen,inits.tarImg)
wall1 = classes.Wall(screen,150,175,10,100,inits.bulImg)
wall2 = classes.Wall(screen,150,screenY-175,10,100,inits.bulImg)
wall3 = classes.Wall(screen,screenX-150,175,10,100,inits.bulImg)
wall4 = classes.Wall(screen,screenX-150,screenY-175,10,100,inits.bulImg)
topBar = classes.Wall(screen,screenX/2,0,screenX,70,inits.bulImg)
trimBar = classes.Wall(screen,screenX/2,423,screenX,50,inits.bulImg)
pygame.key.set_repeat(100,100)

def startScreen():
    crashed = False
    startButtonC = False
    helpButtonC = False
    quitButtonC = False
    screen.fill(inits.red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == MOUSEBUTTONDOWN:
            startButtonC = startButton.clicked()
            helpButtonC = helpButton.clicked()
            quitButtonC = quitButton.clicked()
    if quitButtonC:
        crashed = True
    title.display()
    startButton.display()
    helpButton.display()
    quitButton.display()
    player.display()
    startScreenList = [crashed,startButtonC,helpButtonC]
    return startScreenList

def runScreen(score,speed):
    crashed = False
    died =  False
    screen.fill(inits.red)
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
                bullet = classes.Object(screen,playerxy[0],playerxy[1],inits.bulImg,playerxy[2],bulSpeed)
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
        player.resetrot(90,inits.rubImg)
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

def quitScreen(score,bestScore):
    crashed = False
    retryButtonC = False
    helpButtonC = False
    quitButtonC = False
    screen.fill(inits.red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == MOUSEBUTTONDOWN:
            retryButtonC = retryButton.clicked()
            helpButtonC = helpButton.clicked()
            quitButtonC = quitButton.clicked()
    if quitButtonC:
        crashed = True
    if score >= bestScore:
        bestScore = score
        bestScoretxt.appendText('Best Score: '+str(bestScore))
    endScore.appendText('Score: '+str(score))
    retryButton.display()
    helpButton.display()
    quitButton.display()
    gameOver.display()
    trimBar.display()
    endScore.display()
    bestScoretxt.display()
    quitScreenList = [crashed,retryButtonC,helpButtonC,bestScore]
    return quitScreenList

def helpScreen(stage,speed):
    crashed = False
    nextButtonC = False
    backButtonC = False
    exitButtonC = False
    screen.fill(inits.red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_ESCAPE]:
                exitButtonC = True
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                if stage == 0:
                    player.turn(turnRate)
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                if stage == 0:
                    player.turn(-turnRate)
            if pygame.key.get_pressed()[K_SPACE]:
                bullet = classes.Object(screen,screenX/2,610,inits.bulImg,90,bulSpeed)
                bullets.append(bullet)
        if event.type == MOUSEBUTTONDOWN:
            nextButtonC = nextButton.clicked()
            backButtonC = backButton.clicked()
            if not exitButtonC:
                exitButtonC = exitButton.clicked()
    if nextButtonC:
        if stage < 2:
            stage += 1
            player.resetxy(screenX/2,screenY/2+60)
            player.resetrot(90,inits.playImg)
            speed = 2
    if backButtonC:
        if stage > 0:
            stage -= 1
            player.resetxy(screenX/2,screenY/2+60)
            player.resetrot(90,inits.playImg)
            speed = 2
    exitButton.display()
    helpScreenLine1.display()
    helpScreenLine2.display()
    helpScreenLine3.display()
    if stage == 0:
        player.resetxy(screenX/2,screenY/2+60)
        player.resetrot(90,inits.playImg)
        player.display()
        helpScreenLine1.appendText('This is the Player')
        helpScreenLine2.appendText('Control Him with A & D')
        helpScreenLine3.appendText('or Left & Right')
        nextButton.display()
    if stage == 1:
        target.tarDisplay(screenX/2-12,screenY/2)
        helpScreenLine1.appendText('This is the Target')
        helpScreenLine2.appendText('Use Space to Shoot it')
        helpScreenLine3.appendText('')
        nextButton.display()
        backButton.display()
        for bullet in bullets:
            bullet.move(bulSpeed)
            bullet.display()
            if bullet.objectCollision(target):
                bullets.remove(bullet)
                continue
    if stage == 2:
        player.resetrot(180,inits.playImg)
        helpScreenLine1.appendText('This is a Wall')
        helpScreenLine2.appendText('Don\'t hit it or else')
        helpScreenLine3.appendText('you will die')
        backButton.display()
        if player.objectCollision(wall2):
            player.resetrot(0,inits.rubImg)
            speed = 0
        player.move(speed/2)
        player.display()
        wall2.resetxy(150,screenY-240)
        wall2.display()
    helpScreenList = [crashed,stage,exitButtonC]
    return helpScreenList


while not crashed:
    if stage == 0:
        startScreenList = startScreen()
        crashed = startScreenList[0]
        if startScreenList[1]:
            stage = 1
            continue
        if startScreenList[2]:
            player.resetxy(screenX/2,screenY/2+60)
            player.resetrot(90,inits.playImg)
            speed = 2
            stage = 3
            storedStage = 0
            helpScreenStage = 0
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
        quitScreenList = quitScreen(score,bestScore)
        crashed = quitScreenList[0]
        bestScore = quitScreenList[3]
        if quitScreenList[1]:
            stage = 1
            score = 0
            speed = 2
            gameScore.appendText('Score: '+str(score))
            player = classes.Object(screen,screenX/2,screenY/2+60,inits.playImg,90,speed)
            continue
        if quitScreenList[2]:
            player.resetxy(screenX/2,screenY/2+60)
            player.resetrot(90,inits.playImg)
            speed = 2
            stage = 3
            storedStage = 2
            helpScreenStage = 0
            continue
    elif stage == 3:
        helpScreenList = helpScreen(helpScreenStage,speed)
        crashed = helpScreenList[0]
        helpScreenStage = helpScreenList[1]
        if helpScreenList[2]:
            player.resetxy(screenX/2,screenY/2+60)
            player.resetrot(90,inits.playImg)
            wall2.resetxy(150,screenY-175)
            stage = storedStage
            continue
    pygame.display.update()
    clock.tick(60)
    if died:
        pygame.time.delay(1000)
        died = False