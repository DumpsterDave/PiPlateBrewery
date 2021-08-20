#!/usr/bin/python
import pid
import piplates.THERMOplate as THERMO
import piplates.DAQC2plate as DAQC2
from gpiozero import CPUTemperature
from datetime import datetime
import math
import time
import json
import os
import sys
import signal

run = True

try:
    #Variable Setup
    THERMOPLATEADDR=0  #THERMOPlate Address
    DAQCPLATEADDR=1  #DAQC2Plate Address
    MAINFREQ = 60 #Frequency of Main Power feed (50/60Hz)
    HltPid = pid.PID()
    BkPid = pid.PID()
    
    #Initial Data Load
    f = open('/var/www/html/py/data.json', 'r')
    Data = json.load(f)
    f.close()

    #Set THERMOplate Scale to Farenheit
    THERMO.setSCALE('f')
    #Set our Start Time and next triggers for our SSRs
    startTime = round(time.time(), 1)
    #Set Cycle Length
    CycleLength = MAINFREQ * math.ceil(Data['Global']['Cycle'])

    #Turn on Heatsink Fans
    DAQC2.setDOUTbit(DAQCPLATEADDR, 2)
    DAQC2.setDOUTbit(DAQCPLATEADDR, 3)

    #Set PID Values
    HltPid.kP = Data['HLT']['kp']
    HltPid.kI = Data['HLT']['ki']
    HltPid.kD = Data['HLT']['kd']
    BkPid.kP = Data['BK']['kp']
    BkPid.kI = Data['BK']['ki']
    BkPid.kD = Data['BK']['kd']

    def GetHeatsink(channel):
        global DAQCPLATEADDR
        corrected = 0
        try:
            vRef = DAQC2.getADC(DAQCPLATEADDR,8) * 10
            corrected = (DAQC2.getADC(DAQCPLATEADDR,channel) * vRef)
        except:
            corrected = -1
        return round(corrected, 2)

    def GetCPU():
        cpu = CPUTemperature()
        return cpu.temperature

    def TurnHLTOn():
        global DAQCPLATEADDR
        global Data
        DAQC2.setDOUTbit(DAQCPLATEADDR, 0)
        Data['HLT']['Status'] = 1

    def TurnHLTOff():
        global DAQCPLATEADDR
        global Data
        DAQC2.clrDOUTbit(DAQCPLATEADDR, 0)
        Data['HLT']['Status'] = 0

    def TurnBKOn():
        global DAQCPLATEADDR
        global Data
        DAQC2.setDOUTbit(DAQCPLATEADDR, 1)
        Data['BK']['Status'] = 1

    def TurnBKOff():
        global DAQCPLATEADDR
        global Data
        DAQC2.clrDOUTbit(DAQCPLATEADDR, 1)
        Data['BK']['Status'] = 0

    def OnKill(signum, frame):
        global run, DP
        run = False
        TurnHLTOff()
        TurnBKOff()
        DAQC2.clrDOUTbit(DAQCPLATEADDR, 2)
        DAQC2.clrDOUTbit(DAQCPLATEADDR, 3)

    def UpdateData():
        global Data, HltPid, BkPid
        currTime = round(time.time(), 1)

        #Load Data
        f = open('/var/www/html/py/data.json', 'r')
        Data = json.load(f)
        f.close()

        #Get Temperature Data
        Data['HLT']['HsTemp'] = GetHeatsink(0)
        Data['CPU']['HsTemp'] = GetCPU()
        Data['BK']['HsTemp'] = GetHeatsink(1)
        Data['HLT']['pv'] = THERMO.getTEMP(0,11)
        Data['MT']['pv'] = THERMO.getTEMP(0,10)
        Data['BK']['pv'] = THERMO.getTEMP(0,9)
        
        #Get PID Data
        Data['HLT']['Output'] = HltPid.Output
        Data['HLT']['kp'] = HltPid.kP
        Data['HLT']['ki'] = HltPid.kI
        Data['HLT']['kd'] = HltPid.kD
        Data['HLT']['ITerm'] = HltPid.ITerm
        Data['BK']['Output'] = BkPid.Output
        Data['BK']['kp'] = BkPid.kP
        Data['BK']['ki'] = BkPid.kI
        Data['BK']['kd'] = BkPid.kD
        Data['BK']['ITerm'] = BkPid.ITerm

        #Update Uptime File
        f = open('/var/www/html/py/uptime', 'w')
        f.write(str(currTime - startTime))
        f.close()

        #Check for Updated Targets
            #Mode
        if os.path.exists('/var/www/html/py/mode.json'):
            f = open('/var/www/html/py/mode.json', 'r')
            NewData = json.load(f)
            f.close()
            Data[NewData['Target']]['Mode'] = NewData['NewMode']
            if NewData['Target'] == 'HLT':
                newOut = (Data['HLT']['Manual'] / 100) * MAINFREQ
                HltPid.SetMode(NewData['NewMode'], newOut)
            else:
                newOut = (Data['BK']['Manual'] / 100) * MAINFREQ
                BkPid.SetMode(NewData['NewMode'], newOut)
            os.remove('/var/www/html/py/mode.json')

            #Temp
        if os.path.exists('/var/www/html/py/temp.json'):
            f = open('/var/www/html/py/temp.json', 'r')
            NewData = json.load(f)
            f.close()
            
            if NewData['Mode'] == 0:
                Data[NewData['Target']]['Manual'] = NewData['Value']
                newOut = (NewData['Value'] / 100) * MAINFREQ
                if NewData['Target'] == 'HLT':
                    HltPid.SetMode(0, newOut)
                else:
                    BkPid.SetMode(0, newOut)
            else:
                Data[NewData['Target']]['sv'] = NewData['Value']
            os.remove('/var/www/html/py/temp.json')

            #Settings
        if os.path.exists('/var/www/html/py/settings.json'):
            f = open('/var/www/html/py/settings.json', 'r')
            NewData = json.load(f)
            f.close()
            Data['HLT']['Delta'] = NewData['HLT']['Delta']
            Data['MT']['Delta'] = NewData['MT']['Delta']
            Data['BK']['Delta'] = NewData['BK']['Delta']
            os.remove('/var/www/html/py/settings.json')

        HltPid.SetTarget(Data['HLT']['sv'])
        BkPid.SetTarget(Data['BK']['sv'])
        #Save Data
        f = open('/var/www/html/py/data.json', 'w')
        json.dump(Data, f)
        f.close()

    signal.signal(signal.SIGINT, OnKill)
    signal.signal(signal.SIGTERM, OnKill)

    while run:
        UpdateData()
        HltPid.Compute(Data['HLT']['pv'])
        BkPid.Compute(Data['BK']['pv'])

        HltOff = math.ceil(HltPid.Output * Data['Global']['Cycle'])
        BkOff = math.ceil(BkPid.Output * Data['Global']['Cycle'])

        for i in range(1, CycleLength):
            #Turn SSRs On if off and enabled
            if i == 1:
                if HltPid.Output > 0 and Data['HLT']['Status'] == 0:
                    TurnHLTOn()
                if BkPid.Output > 0 and Data['BK']['Status'] == 0:
                    TurnBKOn()

            if HltOff == i:
                TurnHLTOff()

            if BkOff == i:
                TurnBKOff()

            if i % MAINFREQ == 0:
                UpdateData()

            time.sleep(1 / MAINFREQ)     
       

        #Save Data
        f = open('/var/www/html/py/data.json', 'w')
        json.dump(Data, f)
        f.close()

except KeyboardInterrupt:
    now = datetime.now()
    f = open('/var/www/html/python_errors.log', 'a')
    f.write("%s - TEMP CONTROL [0] - Exit called from Keyboard Interrupt\n" % (now.strftime("%Y-%m-%d %H:%M:%S")))
    f.close()

except Exception as e:
    now = datetime.now()
    print(e)
    f = open('/var/www/html/python_errors.log', 'a')
    f.write("%s - TEMP CONTROL [%i] - %s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), sys.exc_info()[-1].tb_lineno, e))
    f.close()

now = datetime.now()
f = open('/var/www/html/python_errors.log', 'a')
f.write("%s - TEMP CONTROL [0] - Exit called from interface\n" % (now.strftime("%Y-%m-%d %H:%M:%S")))
f.close()