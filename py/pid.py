from collections import deque
import math
import time


class PID(object):

    def __init__(self, P, I, D, CycleLen, MainFreq, SampleFreq):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Sv = 0.0
        self.Pv = 0.0
        self.SampleTime = SampleFreq
        self.LastTime = 0
        self.OutMin = 0
        self.OutMax = math.ceil(CycleLen * MainFreq)
        self.Output = 0
        self.Mode = 1

    def Clamp(self, val):
        ret = val
        if ret > self.OutMax:
            ret = self.OutMax
        elif ret < self.OutMin:
            ret = self.OutMin
        return ret


    def Compute(self, Pv):
        if (self.Mode == 0):
            return
        now = time.monotonic()
        dt = (now - self.LastTime)
        if (dt >= self.SampleTime):
            #Compute Error
            error = self.Sv - Pv
            if error >= 10:
                self.Output = self.OutMax
            elif error <= 0:
                self.Output = self.OutMin
            else:
                p = self.Kp * math.log(error)
                i = 0
                d = 0
                output = p + i + d
                self.Output = self.Clamp(output)

            #Store Variables for next go
            self.LastInput = self.Pv
            self.LastTime = now
    
    def SetTarget(self, Sv):
        self.Sv = Sv

    def SetTunings(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def SetOutputLimits(self, Min, Max):
        if (Min > Max):
            return
        self.OutMin = Min
        self.OutMax = Max

        self.Output = self.Clamp(self.Output)
        
    def SetMode(self, Mode, Output):
        newAuto = (Mode == 1)
        if (newAuto and (self.Mode == 0)):
            self.Initalize()
        else:
            self.Output = math.ceil(Output)
            self.Output = self.Clamp(self.Output)
        self.Mode = Mode
    
    def Initalize(self):
        self.LastInput = self.Pv