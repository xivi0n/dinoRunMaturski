import time

class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.baseX = x
        self.baseY = y
        self.jump = False
        self.crouch = False
        self.gravity = 12
        self.jumpStart = 0

    def reset(self):
        self.x = self.baseX
        self.y = self.baseY
        self.score = 0
        self.jump = False
        self.crouch = False
        self.gravity = 12
        self.jumpStart = 0
    
    def setCrouch(self,state):
        self.crouch = state

    def startJump(self):
        self.gravity = -15
        self.jump = True
        self.jumpStart = time.time()

    def setAnimation(self,sprites):
        if self.jump:
            return "run",1

        elif self.crouch:
            iSprite = (self.score//5)%2
            return "crouch",iSprite

        else:
            iSprite = (self.score//5)%3
            return "run",iSprite
            currSprite = sprites["run"][iSprite]

    def collide(self,objects,screen_width):
        for i in range(3):
            if objects[i][0]<screen_width:
                    if objects[i][1] == 0:
                        if (not self.x+40<objects[i][0]) and (not self.x>objects[i][0]+objects[i][2]*25) and self.y+50>self.baseY:
                            return 1,i
                    if objects[i][1] == 1:
                        if objects[i][2]%2 == 0:
                            if (not self.x+40<objects[i][0]) and (not self.x>objects[i][0]) and self.y+50>self.baseY-8:
                                return 1,i
                        if objects[i][2]%2 == 1:
                            if (not self.x+40<objects[i][0]) and (not self.x>objects[i][0]) and self.y+50>self.baseY-25:#not self.crouch:
                                return 1,i
        return 0,-1

    def move(self,k,sprites):
        
        self.score = self.score + 1

        if self.gravity<12:# and time.time() - self.jumpStart <0.5:
            self.gravity = self.gravity + 1

        # if self.score>400:
        #     print("gravity:",self.gravity)

        if self.jump:
            self.y = self.y + self.gravity
            self.crouch = False
            
        if  self.y > self.baseY:
            self.y = self.baseY
            self.jump = False

        #2 = crouch; 0 = run; 1 = jump; 
        if (k == 1) and not self.jump:
            self.startJump()

        elif (k == 2) and not self.jump:
            self.setCrouch(True)
        
        elif (k == 0) and not self.jump:
            self.setCrouch(False)

        return self.setAnimation(sprites)