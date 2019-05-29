import pygame
import time
import random
from objects import *

display_width = 1200
display_height = 350
CLOCK_SPEED = 60

pygame.init()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('DinoRun')
clock = pygame.time.Clock()

distance = 400
speed = 7

bgcolor = (64,202,201)
fcolor = (244,212,66)
floorH = 50
baseH = display_height-floorH+4-50

sprites = {} #same as spritesI just with pygame objects
spritesI = {
    "floor": ["sprites/floor.png"], #1200x12
    "clouds": ["sprites/clouds.png"], #46x13
    "crouch": ["sprites/crouch1.png","sprites/crouch2.png"], #65x50
    "run": ["sprites/idle.png","sprites/0legup.png","sprites/1legup.png"], #50x50 3px LEFT, RIGHT, 2px DOWN, 1 px UP
    "bird": ["sprites/bird1.png","sprites/bird2.png"], #46x40
    "cactusS": ["sprites/cactusS1.png","sprites/cactusS2.png"], #17x35
    "cactusL": ["sprites/cactusL1.png","sprites/cactusL2.png"]  #25x48
}

def loadAssets():
    global sprites
    for x,y in spritesI.items():
        pom = []
        sprites[x] = pom
        for k in y:
            sprites[x].append(pygame.image.load(k))

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text,x,y):
    largeText = pygame.font.Font('freesansbold.ttf',18)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

def draw(smth,x,y):
    gameDisplay.blit(smth,(x,y))

def drawBG():
    pygame.draw.rect(gameDisplay,bgcolor,[0,0,display_width,display_height-floorH])
    pygame.draw.rect(gameDisplay,fcolor,[0,display_height-floorH,display_width,display_height])
    draw(sprites["floor"][0],0,display_height-floorH)

def drawObj(score):
    for x in objects:
            if x[0]<1200:
                if x[1] == 0:
                    for i in range(x[2]+1):
                        draw(sprites["cactusL"][0],x[0]+25*i,baseH)
                if x[1] == 1:
                    if x[2]%2 == 0:
                        draw(sprites["bird"][(score//5)%2],x[0],baseH-8)
                    if x[2]%2 == 1:
                        draw(sprites["bird"][(score//5)%2],x[0],baseH-25)
            x[0] -= speed
            if x[0]<-100:
                del objects[0]
                objects.append([objects[-1][0]+distance,random.randrange(2),random.randrange(4)])