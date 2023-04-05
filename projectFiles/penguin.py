import math
import tkinter as tk
import time
import random
import ctypes
from win32api import GetMonitorInfo, MonitorFromPoint

IDLE_TO_SLEEP = "IdleToSleep"
IDLE = "Idle"
SLEEP_TO_IDLE = "SleepToIdle"
SLEEP = "Sleep"
WALK_RIGHT = "WalkRight"
WALK_LEFT = "WalkLeft"
DANCE = "Dance"
EAT_COOKIE = "EatCookie"
HATCH = "Hatch"

user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
workArea = (GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")[2], GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")[3])

class AnimState():
    def __init__(self, name, animation, loopTime, minDurration, maxDurration, moveSpeed = 0, loop = True) -> None:
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


class Pet():
    def __init__(self):
        self.kill = False
        self.time = time.time()
        self.deltaTime = 0

        self.width = 100
        self.height = 100
        self.x = random.randint(0, int(workArea[0] - self.width - 50))
        self.y = workArea[1] - self.height

        self.currentSpeed = 0
        self.walkSpeed = 12

        self.stateTimer = 0
        self.state = None
        
        # create a window
        self.window = tk.Tk()
        self.window.bind("<Key>", self.processInput)

        # configure Window and Label
        self.window.config(highlightbackground='blue')  # set focushighlight to black when the window does not have focus
        self.window.overrideredirect(True)  # make window frameless
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'blue')
        self.SetWindowGeometry(self.width, self.height, self.x, self.y)

        hatchAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\hatch.gif', format='gif -index %i' % (i)) for i in range(7)]
        idleToSleepAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\idle-sleep.gif', format='gif -index %i' % (i)) for i in range(3)]
        idleAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\idle.gif', format='gif -index %i' % (i)) for i in range(7)]
        sleepToIdleAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\sleep-idle.gif', format='gif -index %i' % (i)) for i in range(3)]
        sleepAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\sleep.gif', format='gif -index %i' % (i)) for i in range(4)]
        walkRightAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\walk-right.gif', format='gif -index %i' % (i)) for i in range(4)]
        walkLeftAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\walk-left.gif', format='gif -index %i' % (i)) for i in range(4)]
        danceAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\dance.gif', format='gif -index %i' % (i)) for i in range(4)]
        eatCookieAnim = [tk.PhotoImage(file='.\\projectFiles\\images\\eat-cookie.gif', format='gif -index %i' % (i)) for i in range(10)]

        self.states = {
            HATCH: AnimState(HATCH, hatchAnim, 2, 2, 2, loop=False),
            IDLE_TO_SLEEP: AnimState(IDLE_TO_SLEEP, idleToSleepAnim, 1, 1, 1, loop=False),
            IDLE: AnimState(IDLE, idleAnim, 2, 3, 10),
            SLEEP_TO_IDLE: AnimState(SLEEP_TO_IDLE, sleepToIdleAnim, 1, 1, 1, loop=False),
            SLEEP: AnimState(SLEEP, sleepAnim, 2, 3, 15),
            WALK_RIGHT: AnimState(WALK_RIGHT, walkRightAnim, 1, 5, 15, moveSpeed=self.walkSpeed),
            WALK_LEFT: AnimState(WALK_LEFT, walkLeftAnim, 1, 5, 15, moveSpeed=-self.walkSpeed),
            DANCE: AnimState(DANCE, danceAnim, 2, 2, 5),
            EAT_COOKIE: AnimState(EAT_COOKIE, eatCookieAnim, 10, 10, 10, loop=False)
        }

        self.InitState(HATCH)

        # create label to show pet
        self.label = tk.Label(self.window, bd=0, bg='blue')
        self.label.configure(image=self.state.Image())
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.Update)
        self.window.mainloop()

    def SetWindowGeometry(self, width:int, height:int, xPos:int, yPos:int):
        self.window.geometry(f"{width}x{height}+{xPos}+{yPos}")

    def processInput(self, key):
        if key.keycode == 83:
            if self.state.name != IDLE_TO_SLEEP and self.state.name != SLEEP and self.state.name != SLEEP_TO_IDLE:
                self.InitState(IDLE_TO_SLEEP)
            elif self.state.name == SLEEP:
                self.InitState(SLEEP_TO_IDLE)

        elif key.keycode == 27:
            self.kill = True

        elif key.keycode == 68 and self.state.name == IDLE:
            self.InitState(DANCE)

        elif key.keycode == 69:
            self.InitState(EAT_COOKIE)

        elif key.keycode == 72:
            self.InitState(HATCH)

    def Update(self):
        if self.kill:
            self.window.quit()
            return
        
        curTime = time.time()
        self.deltaTime = curTime - self.time
        self.time = curTime

        # update state timer
        self.stateTimer -= self.deltaTime

        if self.stateTimer <= 0:
            self.ChangeState()

        self.state.Update(self.deltaTime)

        # move
        self.x += self.state.moveSpeed
        if self.x < 0 or self.x > screenSize[0] - self.width:
            self.x = min(max(0, self.x), screenSize[0] - self.width)
            self.InitState(WALK_LEFT if self.state.name == WALK_RIGHT else WALK_RIGHT, False)

        # reposition the window
        self.SetWindowGeometry(self.width, self.height, self.x, self.y)

        # add the image to our label
        self.label.configure(image=self.state.Image())

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(int(self.state.frameTime * 1000), self.Update)

    def ChangeState(self):
        if self.state.name == HATCH:
            self.InitState(IDLE)

        elif self.state == self.states[IDLE_TO_SLEEP]:
            self.InitState(SLEEP)

        elif self.state.name in (SLEEP_TO_IDLE, DANCE, EAT_COOKIE):
            self.InitState(IDLE)

        elif self.state == self.states[SLEEP]:
            self.InitState(SLEEP_TO_IDLE)

        elif self.state == self.states[WALK_LEFT] or self.state == self.states[WALK_RIGHT]:
            chance = random.randint(1, 100)
            if chance < 15:
                self.InitState(WALK_LEFT if self.state == self.states[WALK_RIGHT] else WALK_RIGHT)
            else:
                self.InitState(IDLE)

        elif self.state == self.states[IDLE]:
            chance = random.randint(1, 100)
            if chance <= 30:
                self.InitState(WALK_LEFT)
            elif chance <= 60:
                self.InitState(WALK_RIGHT)
            elif chance <= 75:
                self.InitState(IDLE_TO_SLEEP)
            elif chance <= 90:
                self.InitState(DANCE)
            else:
                self.InitState(EAT_COOKIE)

    def InitState(self, newState:str, updateTimer = True):
        self.state = self.states[newState]
        self.state.BeginState()

        if updateTimer:
            self.stateTimer = random.randint(self.state.minDurration, self.state.maxDurration)

        print(f"{newState} - {self.stateTimer}")


Pet()