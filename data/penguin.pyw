import math
import tkinter as tk
import time
import random
import ctypes
from win32api import GetMonitorInfo, MonitorFromPoint
from animState import AnimState
from states import *
from stats import Stats

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

        self.stats = Stats()

        # init timers
        self.hungerTimer = 0
        self.energyTimer = 0
        
        # create a window
        self.window = tk.Tk()

        # configure Window and Label
        self.window.config(highlightbackground='blue')  # set focushighlight to black when the window does not have focus
        self.window.overrideredirect(True)  # make window frameless
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'blue')
        self.SetWindowGeometry(self.width, self.height, self.x, self.y)

        self.animations = {}
        self.state = None

        self.InitState(HatchState())

        # create label to show pet
        self.label = tk.Label(self.window, bd=0, bg='blue')
        self.label.configure(image=self.state.Image())
        self.label.pack()

        # register popup menu
        self.popup_menu = tk.Menu(self.label, tearoff=0)
        self.popup_menu.add_command(label="Feed", command = self.Feed)
        self.popup_menu.add_command(label="Exit", command = self.Kill)
        self.label.bind("<Button-3>", self.Popup)

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.Update)
        self.window.mainloop()

    def Popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def SetWindowGeometry(self, width:int, height:int, xPos:int, yPos:int):
        self.window.geometry(f"{width}x{height}+{xPos}+{yPos}")

    def Update(self):
        if self.kill:
            self.window.quit()
            return

        if self.state.complete:
            self.state = self.state.NextState(self.stats)
        
        curTime = time.time()
        self.deltaTime = curTime - self.time
        self.time = curTime

        # update timers
        self.hungerTimer += self.deltaTime
        self.energyTimer += self.deltaTime

        # increment hunger and energy
        if self.hungerTimer >= 90:
            self.stats.hunger+= 1
            self.hungerTimer = 0
            if self.stats.hunger> 100: self.stats.hunger= 100

        if self.energyTimer >= 180:
            self.stats.energy -= 1
            self.energyTimer = 0
            if self.stats.energy < 0: self.stats.energy = 0

        # update current state
        self.state.UpdateState(self.deltaTime, self.stats)

        # move to new position as indicated by the current state
        if self.state.move:
            self.x += self.state.moveDir * self.walkSpeed
            if self.x < 0 or self.x > screenSize[0] - self.width:
                # turn around if we hit the side of the screen
                self.x = min(max(0, self.x), screenSize[0] - self.width)
                self.state.ExitState(self.stats)
                self.InitState(WalkLeftState() if isinstance(self.state, WalkRightState) else WalkRightState(), self.state.durration)

        # reposition the window
        self.SetWindowGeometry(self.width, self.height, self.x, self.y)

        # add the image to our label
        self.label.configure(image=self.state.Image())

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(int(self.state.frameTime * 1000), self.Update)

    def InitState(self, newState: AnimState, durration = None):
        if self.state:
            self.state.nextState = newState
            self.state.ExitState(self.stats)
        else:
            self.state = newState

        if durration:
            self.state.durration = durration

    def Feed(self):
        self.InitState(EatCookieState())

    def Kill(self):
        self.kill = True


Pet()