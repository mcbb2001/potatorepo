from pygame.locals import *
import pygame
import math
import random

class Text():
    def __init__(self,screen,x,y,font,text,textColor):
        self.screen = screen
        self.text = text
        self.font = font
        self.textColor = textColor
        self.rendText = self.font.render(self.text,False,self.textColor)
        self.width = self.rendText.get_width()
        self.height = self.rendText.get_height()
        self.x = x - self.width/2
        self.y = y

    def display(self):
        self.screen.blit(self.rendText,(self.x,self.y))

    def appendText(self,text):
        self.text = text
        self.rendText = self.font.render(self.text,False,self.textColor)
        self.width = self.rendText.get_width()
        self.height = self.rendText.get_height()
        self.x = x - self.width/2
        self.y = y

class Button():
    def __init__(self,screen,x,y,width,height,color,font,text,textColor):
        self.x = x - width/2
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        self.text = text
        self.font = font
        self.textColor = textColor
        self.rendText = self.font.render(self.text,False,self.textColor)
        self.rendTextWidth = self.rendText.get_width()
        self.rendTextHeight = self.rendText.get_height()

    def display(self):
        pygame.draw.rect(self.screen,self.color,(self.x,self.y,self.width,self.height))
        self.screen.blit(self.rendText,(self.x + (self.width/2 - self.rendTextWidth/2),self.y + (self.height/2-self.rendTextHeight/2)))

    def clicked(self):
        return (pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] >= self.x and pygame.mouse.get_pos()[0] <= self.x + self.width and pygame.mouse.get_pos()[1] >= self.y and pygame.mouse.get_pos()[1] <= self.y + self.height)

class Object():
    def __init__(self,screen,x,y,img,direct):
        self.screen = screen
        self.img = img
        self.dir = direct
        self.width = self.get_rimg().get_width()
        self.height = self.get_rimg().get_height()
        self.x = x - self.width/2
        self.y = y
        self.turnY = y

    def get_rimg(self):
        return pygame.transform.rotate(self.img,self.dir)

    def death(self,direct,img):
        self.dir = direct
        self.img = img

    def turn(self,direct):
        self.dir += direct

    def move(self,speed):
        self.speed = speed
        self.x += self.speed*math.cos(self.dir/180*math.pi)
        self.y -= self.speed*math.sin(self.dir/180*math.pi)

    def resize(self):
        self.img =  pygame.transform.scale(self.img,(int(58-4*self.speed),int(58-4*self.speed)))
        self.width = self.get_rimg().get_width()
        self.height = self.get_rimg().get_height()
    
    def display(self):
        self.screen.blit(self.get_rimg(),(self.x,self.y))

    def axisDisplay(self):
        self.screen.blit(self.get_rimg(),(self.x,self.turnY))

    def borderCollision(self):
        return (self.x <= 0 or self.y <= 0 or self.x+self.width >= self.screen.get_width() or self.y+self.height >= self.screen.get_height())

    def objectCollision(self,other):
        return (other.x <= self.x+self.width and other.x+other.width >= self.x and other.y <= self.y+self.height and other.y+other.height >= self.y)

class Target(Object):
    def __init__(self,screen,img):
        x = (screen.get_width()-24)*random.random()+24
        y = (screen.get_height()-24)*random.random()+24
        super(Target, self).__init__(screen,x,y,img,0)
    
    def random(self):
        self.x = (self.screen.get_width()-24)*random.random()+24
        self.y = (self.screen.get_height()-24)*random.random()+24

class Wall(Object):
    def __init__(self,screen,x,y,width,height,img):
        super(Wall, self).__init__(screen,x,y,pygame.transform.scale(img,(width,height)),0)
