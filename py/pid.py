import math
import time

class PID(object):
    LastTime = 0.0
    LastInput = 0.0
    Input = 0.0
    Output = 0
    SetPoint = 0.0
    ITerm = 0.0
    kP = 1.0
    kI = 0.0
    kD = 0.0
    SampleTime = 1
    OutMin = 0
    OutMax = 60
    Mode = 1

    def __init__(self):
        self.kP = 1.0
        self.kI = 0.0
        self.kD = 0.0
        self.SetPoint = 1.0
        self.SampleTime = 1
        self.OutMin = 0
        self.OutMax = 60

    def Clamp(self, val):
        ret = val
        if ret > self.OutMax:
            ret = self.OutMax
        elif ret < self.OutMin:
            ret = self.OutMin
        return ret


    def Compute(self, pv):
        if (self.Mode == 0):
            return
        now = time.monotonic()
        timeChange = (now - self.LastTime)
        if (timeChange >= self.SampleTime):
            #Compute error variables
            self.Input = pv
            error = self.SetPoint - self.Input
            self.ITerm += (self.kI * error)
            self.ITerm = self.Clamp(self.ITerm)
            dInput = (self.Input - self.LastInput)
            
            #Compute Output
            self.Output = math.ceil(self.kP * error + self.ITerm - self.kD * dInput)
            self.Output = self.Clamp(self.Output)
            #Store Variables for next go
            self.LastInput = self.Input
            self.LastTime = now
    
    def SetTarget(self, sv):
        self.SetPoint = sv

    def SetTunings(self, Kp, Ki, Kd):
        SampleTimeInSec = self.SampleTime / 1000
        self.kP = Kp
        self.kI = Ki * SampleTimeInSec
        self.kD = Kd / SampleTimeInSec

    def SetOutputLimits(self, Min, Max):
        if (Min > Max):
            return
        self.OutMin = Min
        self.OutMax = Max

        self.Output = self.Clamp(self.Output)
        self.ITerm = self.Clamp(self.ITerm)
        
    def SetMode(self, Mode, Output):
        newAuto = (Mode == 1)
        if (newAuto and (self.Mode == 0)):
            self.Initalize()
        else:
            self.Output = math.ceil(Output)
            self.Output = self.Clamp(self.Output)
        self.Mode = Mode
    
    def Initalize(self):
        self.LastInput = self.Input
        self.ITerm = self.Output
        self.ITerm = self.Clamp(self.ITerm)

pid = PID()
pid.SetTarget(168)
pid.kD = 0.2
pid.kP = 1.0
pid.kI = 2.0

for i in range(50,70):
    temp = 110 + i
    pid.Compute(temp)
    print("loop: {}    pidOutput: {}    pidInput: {}".format(i, pid.Output, pid.Input))
    time.sleep(1)