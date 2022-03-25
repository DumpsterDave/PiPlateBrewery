#!/usr/bin/python3
import pid
#import piplates.THERMOplate as THERMO
#import piplates.DAQC2plate as DAQC2
import megaind  #Industrial Automation Card
import librtd  #RTD Data Aquisition Card
from gpiozero import CPUTemperature
from datetime import datetime
import math
import time
import json
import os
import sys
import signal

run = True
error_count = 0

try:
    #Variable Setup
    THERMOPLATEADDR=0   #THERMOPlate Address
    DAQCPLATEADDR=1     #DAQC2Plate Address
    INDADDR = 0         #Industrial Automation Card Address
    RTDADDR = 1         #RTD Data Aquisition Card Address
    MAINFREQ = 60 #Frequency of Main Power feed (50/60Hz)
    
    #Initial Data Load
    f = open('/var/www/html/py/data.json', 'r')
    Data = json.load(f)
    f.close()

    #Set THERMOplate Scale to Farenheit
    #THERMO.setSCALE('f')
    
    #Set our Start Time and next triggers for our SSRs
    startTime = round(time.time(), 1)
    #Set Cycle Length
    CycleLength = Data['Global']['Cycle']
    LoopMax = CycleLength * MAINFREQ

    #Setup PID Controllers
    HltPid = pid.PID(Data['HLT']['Kp'], Data['HLT']['Ki'], Data['HLT']['Kd'], CycleLength, MAINFREQ, 1)
    BkPid = pid.PID(Data['BK']['Kp'], Data['BK']['Ki'], Data['BK']['Kd'], CycleLength, MAINFREQ, 1)
    HltPid.SetOutputLimits(Data['HLT']['OutMinPct'] * LoopMax, Data['HLT']['OutMaxPct'] * LoopMax)
    BkPid.SetOutputLimits(Data['BK']['OutMinPct'] * LoopMax, Data['BK']['OutMaxPct'] * LoopMax)

    #Turn on Heatsink Fans
    #DAQC2.setDOUTbit(DAQCPLATEADDR, 2)
    #DAQC2.setDOUTbit(DAQCPLATEADDR, 3)
    
    megaind.setOdPWM(INDADDR, 3, 100)

    def GetRTD(channel, scale):
        global RTDADDR
        TempCel = librtd.get(RTDADDR, channel)
        TempRet = TempCel
        if scale == 'f':
            TempRet = (TempCel * 1.8) + 32
        if scale == 'k':
            TempRet = TempCel + 273.15
        return TempRet

    def GetHeatsink(channel):
        #global DAQCPLATEADDR
        #corrected = 0
        #try:
            #vRef = DAQC2.getADC(DAQCPLATEADDR,8) * 10
            #corrected = (DAQC2.getADC(DAQCPLATEADDR,channel) * vRef)
        #except:
            #corrected = -1
        #return round(corrected, 2)
        return GetRTD(channel, 'c')

    def GetCPU():
        cpu = CPUTemperature()
        return cpu.temperature

    def TurnHLTOn():
        global DAQCPLATEADDR
        global INDADDR
        global Data
        #DAQC2.setDOUTbit(DAQCPLATEADDR, 0)
        megaind.setOdPWM(INDADDR, 1, 100)
        Data['HLT']['Status'] = 1

    def TurnHLTOff():
        global DAQCPLATEADDR
        global INDADDR
        global Data
        #DAQC2.clrDOUTbit(DAQCPLATEADDR, 0)
        megaind.setOdPWM(INDADDR, 1, 0)
        Data['HLT']['Status'] = 0

    def TurnBKOn():
        global DAQCPLATEADDR
        global INDADDR
        global Data
        #DAQC2.setDOUTbit(DAQCPLATEADDR, 1)
        megaind.setOdPWM(INDADDR, 2, 100)
        Data['BK']['Status'] = 1

    def TurnBKOff():
        global DAQCPLATEADDR
        global INDADDR
        global Data
        #DAQC2.clrDOUTbit(DAQCPLATEADDR, 1)
        megaind.setOdPWM(INDADDR, 2, 0)
        Data['BK']['Status'] = 0

    def OnKill(signum, frame):
        global run, DP, INDADDR
        run = False
        TurnHLTOff()
        TurnBKOff()
        #DAQC2.clrDOUTbit(DAQCPLATEADDR, 2)
        #DAQC2.clrDOUTbit(DAQCPLATEADDR, 3)
        megaind.setOdPWM(INDADDR, 3, 0)
        megaind.setOdPWM(INDADDR, 4, 0)

    def UpdateData():
        global Data, HltPid, BkPid
        currTime = round(time.time(), 1)

        #Load Data
        f = open('/var/www/html/py/data.json', 'r')
        Data = json.load(f)
        f.close()

        #Get Temperature Data
        Data['HLT']['HsTemp'] = GetHeatsink(4)
        Data['CPU']['HsTemp'] = GetCPU()
        Data['BK']['HsTemp'] = GetHeatsink(5)
        #Data['HLT']['Pv'] = THERMO.getTEMP(0,11)
        #Data['MT']['Pv'] = THERMO.getTEMP(0,10)
        #Data['BK']['Pv'] = THERMO.getTEMP(0,9)
        Data['HLT']['Pv'] = GetRTD(1, 'f')
        Data['MT']['Pv'] = GetRTD(2, 'f')
        Data['BK']['Pv'] = GetRTD(3, 'f')
        
        #Get PID Data
        Data['HLT']['Output'] = HltPid.Output
        Data['HLT']['Kp'] = HltPid.Kp
        Data['HLT']['Ki'] = HltPid.Ki
        Data['HLT']['Kd'] = HltPid.Kd
        #Data['HLT']['ITerm'] = HltPid.ITerm
        Data['BK']['Output'] = BkPid.Output
        Data['BK']['Kp'] = BkPid.Kp
        Data['BK']['Ki'] = BkPid.Ki
        Data['BK']['Kd'] = BkPid.Kd
        #Data['BK']['ITerm'] = BkPid.ITerm

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
                newOut = (Data['HLT']['Manual'] / 100) * MAINFREQ * CycleLength
                HltPid.SetMode(NewData['NewMode'], newOut)
            else:
                newOut = (Data['BK']['Manual'] / 100) * MAINFREQ * CycleLength
                BkPid.SetMode(NewData['NewMode'], newOut)
            os.remove('/var/www/html/py/mode.json')

            #Temp
        if os.path.exists('/var/www/html/py/temp.json'):
            f = open('/var/www/html/py/temp.json', 'r')
            NewData = json.load(f)
            f.close()
            
            if NewData['Mode'] == 0:
                Data[NewData['Target']]['Manual'] = NewData['Value']
                newOut = (NewData['Value'] / 100) * MAINFREQ * CycleLength
                if NewData['Target'] == 'HLT':
                    HltPid.SetMode(0, newOut)
                else:
                    BkPid.SetMode(0, newOut)
            else:
                Data[NewData['Target']]['Sv'] = NewData['Value']
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

        HltPid.SetTarget(Data['HLT']['Sv'])
        BkPid.SetTarget(Data['BK']['Sv'])
        #Save Data
        f = open('/var/www/html/py/data.json', 'w')
        json.dump(Data, f)
        f.close()

    signal.signal(signal.SIGINT, OnKill)
    signal.signal(signal.SIGTERM, OnKill)

    while run:
        UpdateData()
        if error_count > 0:
            megaind.setOdPWM(INDADDR, 4, 100)
        else:
            megaind.setOdPWM(INDADDR, 4, 0)
            
        HltPid.Compute(Data['HLT']['Pv'])
        BkPid.Compute(Data['BK']['Pv'])

        for i in range(1, LoopMax):
            #Turn SSRs On if off and enabled
            if i == 1:
                if HltPid.Output > 0 and Data['HLT']['Status'] == 0:
                    TurnHLTOn()
                if BkPid.Output > 0 and Data['BK']['Status'] == 0:
                    TurnBKOn()

            if HltPid.Output == i:
                TurnHLTOff()

            if BkPid.Output == i:
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
    error_count += 1

now = datetime.now()
f = open('/var/www/html/python_errors.log', 'a')
f.write("%s - TEMP CONTROL [0] - Exit called from interface\n" % (now.strftime("%Y-%m-%d %H:%M:%S")))
f.close()
