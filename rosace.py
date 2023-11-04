import pygame as pg
import sys
import numpy as np
from math import *

winsize = 800
display = pg.display.set_mode((winsize,winsize))
clock = pg.time.Clock()
win = np.array([float(winsize/2),float(winsize/2)])

points = []

def rotmat(angle):
    nx = cos(angle)-sin(angle)
    ny = sin(angle)+cos(angle)
    return np.array([[cos(angle),-sin(angle)],\
                     [sin(angle),cos(angle)]])

def mult(pos,angle):
    #get new position from a certain angle using sin and cos
    x,y=pos[0],pos[1]
    nx = cos(angle)*x-sin(angle)*y
    ny = sin(angle)*x+cos(angle)*y
    return [nx,ny]

class Rotator:
    def __init__(self, dist, speed, color="white"):
        self.pos = np.array([0.0,float(dist)])
        self.dpos = np.array([0.0,float(dist)])
        self.angle = speed/1000
        self.father = None
        self.child = None
        self.color = color
        self.drawing = True
    
    def draw(self):
        global points
        self.pos = mult(self.pos, self.angle)
        self.dpos = np.array([x for x in self.pos])
        if self.father != None:
            self.dpos += self.father.dpos
            #pg.draw.line(display, "white", self.dpos+win, self.father.dpos+win, 1)
            if (self.child is None) or (self.drawing):
                pg.draw.circle(display, self.color, self.dpos+win, 1)
                pass
        else:
            #pg.draw.line(display, "white", self.pos+win, win, 1)
            if (self.child is None) or (self.drawing):
                pg.draw.circle(display, self.color, self.pos + win, 1)
                pass
        
        if self.child != None:
            self.child.draw()
    
    def addChild(self,child,draws=False):
        self.drawing = draws
        if self.child != None:
            self.child.addChild(child,draws)
        else:
            self.child = child
            self.child.father = self

objects = []
rotat = Rotator(100,10)
rotat.addChild(Rotator(30,20))
rotat.addChild(Rotator(25,30))
objects.append(rotat)

while True:
    #display.fill((0,0,0))


    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    for obj in objects:
        obj.draw()

    clock.tick(500)
    pg.display.update()