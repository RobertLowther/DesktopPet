import random
import tkinter as tk
from animState import AnimState
from stats import Stats

class HatchState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.loop = False
        self.animation = [tk.PhotoImage(file='.\\data\\images\\hatch.gif', format='gif -index %i' % (i)) for i in range(7)]
        self.frameCount = len(self.animation)
        self.loopTime = 2
        self.minDurration = 2
        self.maxDurration = 2
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState

        return IdleState()

class IdleState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\idle.gif', format='gif -index %i' % (i)) for i in range(7)]
        self.frameCount = len(self.animation)
        self.loopTime = 2
        self.minDurration = 3
        self.maxDurration = 10
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState

        chance = random.randint(1, 100)

        if stats.energy <= 15:
            return IdleToSleepState()
        elif stats.hunger >= 80:
            return CryState()
        elif chance <= 42:
            return WalkLeftState()
        elif chance <= 85:
            return WalkRightState()
        else:
            if stats.hunger < 50:
                return DanceState()
            else:
                return CryState()

class CryState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\cry.gif', format='gif -index %i' % (i)) for i in range(7)]
        self.frameCount = len(self.animation)
        self.loopTime = 2
        self.minDurration = 3
        self.maxDurration = 10
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return IdleState()

class DanceState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\dance.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.frameCount = len(self.animation)
        self.loopTime = 2
        self.minDurration = 2
        self.maxDurration = 5
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return IdleState()

class WalkRightState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\walk-right.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.frameCount = len(self.animation)
        self.loopTime = 1
        self.minDurration = 5
        self.maxDurration = 15
        self.frameTime = self.loopTime / self.frameCount
        self.move = True
        self.moveDir = 1
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        chance = random.randint(1, 100)
        if chance < 15:
            return WalkLeftState()
        else:
            return IdleState()

class WalkLeftState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\walk-left.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.frameCount = len(self.animation)
        self.loopTime = 1
        self.minDurration = 5
        self.maxDurration = 15
        self.frameTime = self.loopTime / self.frameCount
        self.move = True
        self.moveDir = -1
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        chance = random.randint(1, 100)
        if chance < 15:
            return WalkRightState()
        else:
            return IdleState()

class IdleToSleepState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.loop = False
        self.animation = [tk.PhotoImage(file='.\\data\\images\\idle-sleep.gif', format='gif -index %i' % (i)) for i in range(3)]
        self.frameCount = len(self.animation)
        self.loopTime = 1
        self.minDurration = 1
        self.maxDurration = 1
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return SleepState()
        
class SleepToIdleState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.loop = False
        self.animation = [tk.PhotoImage(file='.\\data\\images\\idle-sleep.gif', format='gif -index %i' % (i)) for i in range(3)]
        self.frameCount = len(self.animation)
        self.loopTime = 1
        self.minDurration = 1
        self.maxDurration = 1
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return IdleState()
        
class SleepState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.animation = [tk.PhotoImage(file='.\\data\\images\\sleep.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.frameCount = len(self.animation)
        self.loopTime = 2
        self.minDurration = 3
        self.maxDurration = 15
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
        stats.energy = 100
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return SleepToIdleState()
        
class EatCookieState(AnimState):
    def __init__(self) -> None:
        super().__init__()

        self.loop = False
        self.animation = [tk.PhotoImage(file='.\\data\\images\\eat-cookie.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.frameCount = len(self.animation)
        self.loopTime = 10
        self.minDurration = 10
        self.maxDurration = 10
        self.frameTime = self.loopTime / self.frameCount
        self.EnterState()

    def EnterState(self):
        super().EnterState()

    def UpdateState(self, deltaTime: float, stats: Stats):
        super().UpdateState(deltaTime, stats)

    def ExitState(self, stats: Stats):
        super().ExitState(stats)
        stats.hunger = 0
        stats.energy = 15
    
    def NextState(self, stats: Stats):
        if self.nextState: return self.nextState
        
        return SleepToIdleState()