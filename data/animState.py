import random
from stats import Stats

class AnimState():
    def __init__(self) -> None:
        self.loop = True
        self.move = False
        self.moveDir = 0
        self.minDurration = None
        self.maxDurration = None
        self.durration = None
        self.animation = None
        self.frameCount = None
        self.loopTime = None
        self.frameTime = None

        self.currentFrame = 0
        self.frameTimer = 0
        self.stateTimer = 0
        self.complete = False
        self.nextState = None

    def EnterState(self):
        self.durration = random.randint(self.minDurration, self.maxDurration)

    def UpdateState(self, deltaTime, stats: Stats):        
        self.frameTimer += deltaTime
        if self.frameTimer >= self.frameTime:
            self.frameTimer -= self.frameTime
            self.currentFrame = (self.currentFrame + 1) % self.frameCount

            if self.loop == False and self.currentFrame == 0:
                self.currentFrame = len(self.animation) - 1

        self.stateTimer += deltaTime
        try:
            if self.stateTimer >= self.durration:
                self.ExitState(stats)
        except:
            print()
    
    def ExitState(self, stats: Stats):
        self.complete = True

    def NextState(self, stats: Stats):
        pass

    def Image(self):
        return self.animation[self.currentFrame]
