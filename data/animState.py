import tkinter as tk

class AnimState():
    def __init__(self, name:str, animation:tk.PhotoImage, loopTime:int, minDurration:int, maxDurration:int, moveSpeed:int = 0, loop:bool = True) -> None:
        self.name = name
        self.loop = loop
        self.minDurration = minDurration
        self.maxDurration = maxDurration
        self.animation = animation
        self.frameCount = len(animation)
        self.loopTime = loopTime
        self.frameTime = loopTime / self.frameCount
        self.moveSpeed = moveSpeed

        self.currentFrame = 0
        self.frameTimer = 0

    def Update(self, deltaTime):        
        self.frameTimer += deltaTime
        if self.frameTimer >= self.frameTime:
            self.frameTimer -= self.frameTime
            self.currentFrame = (self.currentFrame + 1) % self.frameCount

            if self.loop == False and self.currentFrame == 0:
                self.currentFrame = len(self.animation) - 1

    def BeginState(self):
        self.currentFrame = 0
        self.frameTimer = 0

    def Image(self):
        return self.animation[self.currentFrame]
