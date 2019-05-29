import random
objects = []

def predefineObjects(distance):
    global objects
    for i in range(0,10):
        objects.append([1200+i*distance,random.randrange(2),random.randrange(4)])

def resetObjects():
    global objects
    del objects[:]

def closest(X):
    for i in range(len(objects)):
        if (objects[i][0]-X>0):
             return i