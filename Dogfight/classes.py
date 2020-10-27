from pygame.locals import *
import pygame
import math
import random

#hello

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
        self.x2 = x

    def display(self):
        self.screen.blit(self.rendText,(self.x,self.y))

    def appendText(self,text):
        self.text = text
        self.rendText = self.font.render(self.text,False,self.textColor)
        self.width = self.rendText.get_width()
        self.height = self.rendText.get_height()
        self.x = self.x2 - self.width/2

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
    def __init__(self,screen,x,y,img,direct,speed):
        self.screen = screen
        self.img = img
        self.dir = direct
        self.speed = speed
        self.width = self.get_rimg().get_width()
        self.height = self.get_rimg().get_height()
        self.x = x
        self.y = y 

    def get_rimg(self):
        return pygame.transform.rotate(self.img,self.dir)

    def get_xy(self):
        return [self.x,self.y,self.dir]

    def resetrot(self,direct,img):
        self.dir = direct
        self.img = img

    def resetxy(self,x,y):
        self.x = x
        self.y = y

    def turn(self,direct):
        self.dir += direct

    def move(self,speed):
        self.speed = speed
        self.x += self.speed*math.cos(self.dir/180*math.pi)
        self.y -= self.speed*math.sin(self.dir/180*math.pi)
    
    def display(self):
        img = self.get_rimg()
        x = int(self.x-(img.get_width())/2)
        y = int(self.y-(img.get_height())/2)
        self.screen.blit(img,(x,y))

    def borderCollision(self):
        return (self.x-self.width/2 <= 0 or self.y-self.height/2 <= 0 or self.x+self.width/2 >= self.screen.get_width() or self.y+self.height/2 >= self.screen.get_height())

    def objectCollision(self,other):
        return (self.x+self.width/2 >= other.x-other.width/2 and self.x-self.width/2 <= other.x+other.width/2 and self.y-self.height/2 <= other.y+other.height/2 and self.y+self.height/2 >= other.y-other.height/2)

class Target(Object):
    def __init__(self,screen,img):
        x = (screen.get_width()-24)*random.random()+24
        y = (screen.get_height()-24)*random.random()+24
        super(Target, self).__init__(screen,x,y,img,0,0)
    
    def random(self):
        self.x = (self.screen.get_width()-24)*random.random()+24
        self.y = (self.screen.get_height()-24)*random.random()+24

    def tarDisplay(self,x,y):
        self.x = x
        self.y = y
        self.screen.blit(self.get_rimg(),(x,y))

class Wall(Object):
    def __init__(self,screen,x,y,width,height,img):
        super(Wall, self).__init__(screen,x,y,pygame.transform.scale(img,(width,height)),0,0)

class Ai(Object):
    def __init__(self,screen,x,y,img,direct,speed,lookahead):
        super(Ai,self).__init__(screen,x,y,img,direct,speed)
        self.lookX = self.x + lookahead*math.cos(self.dir/180*math.pi)
        self.lookY = self.y + lookahead*math.sin(self.dir/180*math.pi)

    def aiBorderCollision(self):
        return (self.lookX-self.width/2 <= 0 or self.lookY-self.height/2 <= 0 or self.lookX+self.width/2 >= self.screen.get_width() or self.lookY+self.height/2 >= self.screen.get_height())

    def aiObjectCollision(self,other):
        return (self.lookX+self.width/2 >= other.x-other.width/2 and self.lookX-self.width/2 <= other.x+other.width/2 and self.lookY-self.height/2 <= other.y+other.height/2 and self.lookY+self.height/2 >= other.y-other.height/2)
