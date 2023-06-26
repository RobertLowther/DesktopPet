import math
import tkinter as tk
import time
import random
import ctypes
from win32api import GetMonitorInfo, MonitorFromPoint
from animState import AnimState

IDLE_TO_SLEEP = "IdleToSleep"
IDLE = "Idle"
SLEEP_TO_IDLE = "SleepToIdle"
SLEEP = "Sleep"
WALK_RIGHT = "WalkRight"
WALK_LEFT = "WalkLeft"
DANCE = "Dance"
EAT_COOKIE = "EatCookie"
HATCH = "Hatch"
CRY = "Cry"

user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
workArea = (GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")[2], GetMonitorInfo(MonitorFromPoint((0,0))).get("Work")[3])

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

        self.energy = 100
        self.hunger = 0

        # init timers
        self.stateTimer = 0
        self.hungerTimer = 0
        self.energyTimer = 0

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

        self.animations = {}
        self.states = {}

        # setup states and animations
        self.RegisterAnimations()
        self.RegisterStates()

        self.InitState(HATCH)

        # create label to show pet
        self.label = tk.Label(self.window, bd=0, bg='blue')
        self.label.configure(image=self.state.Image())
        self.label.pack()

        # register popup menu
        self.popup_menu = tk.Menu(self.label, tearoff=0)
        self.popup_menu.add_command(label="Feed", command = self.Feed)
        self.popup_menu.add_command(label="Kill", command = self.Kill)
        self.label.bind("<Button-3>", self.Popup)

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.Update)
        self.window.mainloop()

    def Popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def RegisterAnimations(self):
        self.animations["hatchAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\hatch.gif', format='gif -index %i' % (i)) for i in range(7)]
        self.animations["idleToSleepAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\idle-sleep.gif', format='gif -index %i' % (i)) for i in range(3)]
        self.animations["idleAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\idle.gif', format='gif -index %i' % (i)) for i in range(7)]
        self.animations["sleepToIdleAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\sleep-idle.gif', format='gif -index %i' % (i)) for i in range(3)]
        self.animations["sleepAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\sleep.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.animations["walkRightAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\walk-right.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.animations["walkLeftAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\walk-left.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.animations["danceAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\dance.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.animations["eatCookieAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\eat-cookie.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.animations["cryAnim"] = [tk.PhotoImage(file='.\\projectFiles\\images\\cry.gif', format='gif -index %i' % (i)) for i in range(7)]

    def RegisterStates(self):
        self.states[HATCH] = AnimState(HATCH, self.animations["hatchAnim"], 2, 2, 2, loop=False)
        self.states[IDLE_TO_SLEEP] = AnimState(IDLE_TO_SLEEP, self.animations["idleToSleepAnim"], 1, 1, 1, loop=False)
        self.states[IDLE] = AnimState(IDLE, self.animations["idleAnim"], 2, 3, 10)
        self.states[SLEEP_TO_IDLE] = AnimState(SLEEP_TO_IDLE, self.animations["sleepToIdleAnim"], 1, 1, 1, loop=False)
        self.states[SLEEP] = AnimState(SLEEP, self.animations["sleepAnim"], 2, 3, 15)
        self.states[WALK_RIGHT] = AnimState(WALK_RIGHT, self.animations["walkRightAnim"], 1, 5, 15, moveSpeed=self.walkSpeed)
        self.states[WALK_LEFT] = AnimState(WALK_LEFT, self.animations["walkLeftAnim"], 1, 5, 15, moveSpeed=-self.walkSpeed)
        self.states[DANCE] = AnimState(DANCE, self.animations["danceAnim"], 2, 2, 5)
        self.states[EAT_COOKIE] = AnimState(EAT_COOKIE, self.animations["eatCookieAnim"], 10, 10, 10, loop=False)
        self.states[CRY] = AnimState(CRY, self.animations["cryAnim"], 2, 3, 10)

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

        elif key.keycode == 81:
            self.InitState(CRY)

        elif key.keycode == 68 and self.state.name == IDLE:
            self.InitState(DANCE)

        elif key.keycode == 69:
            self.InitState(EAT_COOKIE)

        elif key.keycode == 72:
            self.InitState(HATCH)
        elif key.keycode == 9:
            self.InitState(IDLE)

    def Update(self):
        if self.kill:
            self.window.quit()
            return
        
        curTime = time.time()
        self.deltaTime = curTime - self.time
        self.time = curTime

        # update timers
        self.stateTimer -= self.deltaTime
        self.hungerTimer += self.deltaTime
        self.energyTimer += self.deltaTime

        # increment hunger and energy
        if self.hungerTimer >= 90:
            self.hunger += 1
            self.hungerTimer = 0

        if self.energyTimer >= 180:
            self.energy -= 1
            self.energyTimer = 0

        # switch state when this one ends
        if self.stateTimer <= 0:
            self.ChangeState()

        # update current state
        self.state.Update(self.deltaTime)

        # move to new position as indicated by the current state
        self.x += self.state.moveSpeed
        if self.x < 0 or self.x > screenSize[0] - self.width:
            self.x = min(max(0, self.x), screenSize[0] - self.width)
            # turn around if we hit the side of the screen
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

        elif self.state.name in (SLEEP_TO_IDLE, DANCE, EAT_COOKIE, CRY):
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

            if self.energy <= 15:
                self.Sleep()
            elif self.hunger >= 80:
                self.InitState(CRY)

            elif chance <= 35:
                self.InitState(WALK_LEFT)
            elif chance <= 70:
                self.InitState(WALK_RIGHT)
            elif chance <= 85:
                self.InitState(IDLE_TO_SLEEP)
            else:
                if self.hunger < 50:
                    self.InitState(DANCE)
                else:
                    self.InitState(CRY)

    def InitState(self, newState:str, updateTimer = True):
        self.state = self.states[newState]
        self.state.BeginState()

        if updateTimer:
            self.stateTimer = random.randint(self.state.minDurration, self.state.maxDurration)

        #print(f"{newState} - {self.stateTimer}")

    def Feed(self):
        self.InitState(EAT_COOKIE)
        self.huger = 0
        print(f"hunger: {self.hunger}")

    def Sleep(self):
        self.InitState(IDLE_TO_SLEEP)
        self.energy = 100
        self.energyTimer = 0
        print(f"energy: {self.energy}")

    def Kill(self):
        self.kill = True


Pet()