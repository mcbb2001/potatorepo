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
speed = 2
bulSpeed = 10
score = 0
bestScore = 0
rectHeight = 30

#colors:
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

#fonts:
gameFont = pygame.font.SysFont('Arial', 30)
titleFont = pygame.font.SysFont('Arial', 60)
endFont = pygame.font.SysFont('Arial', 40)

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
gameDisplay = pygame.display.set_mode((disX,disY))

#create game clock
clock = pygame.time.Clock()

class Title():
    def __init__(self,screen,x,y,text):
        self.x = x
        self.y = y
        self.text = text

    def display(self,screen):
        screen.blit(titleFont.render(self.text,False,black),(self.x,self.y))

class Button():
    def __init__(self,x,y,xdis,ydis,width,height,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.xdis = xdis
        self.ydis = ydis

    def display(self,screen):
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height))
        screen.blit(gameFont.render(self.text,False,red),(self.x+self.xdis,self.y+self.ydis))
        
    def clicked(self,screen):
        clicked = False
        if pygame.mouse.get_pos()[0] >= self.x and pygame.mouse.get_pos()[0] <= self.x+self.width and pygame.mouse.get_pos()[1] >= self.y and pygame.mouse.get_pos()[1] <= self.y+self.height:
            clicked = True
        return clicked

class Object():
    def __init__(self,playX,playY,playImg,playdir):
        self.x = playX
        self.y = playY
        self.img = playImg
        self.dir = playdir
        self.get_width = self.get_rimg().get_width
        self.get_height = self.get_rimg().get_height

    def turn(self,playdir):
        self.dir += playdir

    def resetRotation(self,direction):
        self.dir = direction

    def move(self,speed,playImg):
        self.x += speed*math.cos(self.dir/180*math.pi)
        self.y += speed*-math.sin(self.dir/180*math.pi)

    def resize(self,speed,playImg):
        self.img = pygame.transform.scale(playImg,(int(58-4*speed),int(58-4*speed)))
        self.get_width = self.get_rimg().get_width
        self.get_height = self.get_rimg().get_height

    def get_rimg(self):
        return pygame.transform.rotate(self.img, self.dir)
    
    def display(self,screen):
        rimg = self.get_rimg()
        screen.blit(rimg, (int(self.x - (rimg.get_width() / 2)), int(self.y - (rimg.get_height() / 2))))

    def borderCollision(self,screen):
        return (self.x - self.get_width()/2 <= 0 or self.y - self.get_height()/2 <= rectHeight or self.x + self.get_width()/2 >= screen.get_width() or self.y + self.get_height()/2 >= screen.get_height())

    def objectCollision(self,other):
        return (other.x-other.get_width()/2 <= self.x+self.get_width()/2 and other.x+other.get_width()/2 >= self.x-self.get_width()/2 and other.y-other.get_height()/2 <= self.y+self.get_height()/2 and other.y+other.get_height()/2 >= self.y-self.get_height()/2)

class Target(Object):
    def __init__(self,tarImg,screen):
        x = (screen.get_width()-24)*random.random()+24
        y = (screen.get_height()-rectHeight-24)*random.random()+rectHeight+24
        super(Target, self).__init__(x,y,tarImg,0)
    
    def shot(self,screen):
        self.x = (screen.get_width()-24)*random.random()+24
        self.y = (screen.get_height()-rectHeight-24)*random.random()+rectHeight+24

class Wall(Object):
    def __init__(self,screen,x,y,width,height):
        super(Wall, self).__init__(x,y,pygame.transform.scale(bulImg,(width,height)),0)

class TopBar():
    def __init__(self,screen,gameFont):
        self.x = 0
        self.y = 0
        self.width = screen.get_width()
        self.height = rectHeight

    def display(self,screen,score):
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height))
        screen.blit(gameFont.render('Score: '+str(score),False,red),(0,0))

class ScoreBar():
    def __init__(self,screen,yoff,height):
        self.x = 0
        self.y = yoff
        self.width = screen.get_width()
        self.height = height

    def display(self,screen,score):
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height))
        screen.blit(endFont.render('Score: '+str(score),False,red),(screen.get_width()/2-75,self.y+5))

class BestScore():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bestScore = bestScore

    def display(self,screen):
        screen.blit(gameFont.render('Best Score: '+str(self.bestScore),False,black),(self.x,self.y))
    
    def appendBestScore(self,bestScore):
        self.bestScore = bestScore

    def getBestScore(self):
        return self.bestScore

title = Title(gameDisplay,140,50,'Dogfight')
startButton = Button(200,135,18,8,100,50,'Start')
helpButton = Button(200,200,20,8,100,50,'Help')

bullets = []

topBar = TopBar(gameDisplay,gameFont)
plane = Object(playX,playY,playImg,90)
target = Target(tarImg,gameDisplay)
wall1 = Wall(gameDisplay,150,200,10,100)
wall2 = Wall(gameDisplay,disX-160,200,10,100)
wall3 = Wall(gameDisplay,150,disY-200,10,100)
wall4 = Wall(gameDisplay,disX-160,disY-200,10,100)

gameOverText = Title(gameDisplay,100,50,'Game Over')
restartButton = Button(200,135,15,8,100,50,'Retry')
quitButton = Button(200,265,22,8,100,50,'Quit')
scoreBar = ScoreBar(gameDisplay,400,60)
bestScore = BestScore(160,470)

pygame.key.set_repeat(100,100)

def start():
    crashed = False
    startClicked = False
    helpClicked = False
    gameDisplay.fill(red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if pygame.mouse.get_pressed()[0]:
            startClicked = startButton.clicked(gameDisplay)
            helpClicked = helpButton.clicked(gameDisplay)
    title.display(gameDisplay)
    plane.display(gameDisplay)
    startList = [crashed,startClicked,helpClicked]
    startButton.display(gameDisplay)
    helpButton.display(gameDisplay)
    return startList

def run(score,speed):
    playerImg = playImg
    died = False
    crashed = False
    gameDisplay.fill(red)
    for event in pygame.event.get():
        if event.type == QUIT:
            crashed = True
        if event.type == KEYDOWN:
            pygame.key.get_pressed()
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                plane.turn(playdir)
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                plane.turn(-playdir)
            if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
                if speed <= 5:
                    speed += 0.5
            if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
                if speed >= 1:
                    speed -= 0.5
            if pygame.key.get_pressed()[K_SPACE]:
                bullets.append(Object(plane.x,plane.y,bulImg,plane.dir))
    while target.objectCollision(wall1) or target.objectCollision(wall2) or target.objectCollision(wall3) or target.objectCollision(wall4):
        target.shot(gameDisplay)
    for bullet in bullets:
        bullet.move(bulSpeed,bulImg)
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
        died = True
    if plane.objectCollision(wall1) or plane.objectCollision(wall2) or plane.objectCollision(wall3) or plane.objectCollision(wall4):
        died = True
    if died:
        playerImg = rubImg
        speed = 0
        plane.resetRotation(90)
    wall1.display(gameDisplay)
    wall2.display(gameDisplay)
    wall3.display(gameDisplay)
    wall4.display(gameDisplay)
    topBar.display(gameDisplay,score)
    target.display(gameDisplay)
    plane.move(speed,playerImg)
    plane.resize(speed,playerImg)
    runList = [crashed,score,speed,died]
    plane.display(gameDisplay)
    return runList

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
        gamestats = start()
        crashed = gamestats[0]
        if gamestats[1]:
            stage = 1
            continue
    elif stage == 1:
        runList = run(score,speed)
        crashed = runList[0]
        score = runList[1]
        speed = runList[2]
        died = runList[3]
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