#!/usr/bin/python
import piplates.THERMOplate as THERMO
import piplates.DAQC2plate as DAQC2
from gpiozero import CPUTemperature
from datetime import datetime
import time
import math
import json

try:
    #Variable Setup
    TP=0
    DP=1
    UpdateTemps = True
    ActionCount = 0
    HLTOn = -1
    HLTOff = -1
    BKOn = -1
    BKOff = -1
    
    f = open('/var/www/html/py/data.json', 'r')
    data = json.load(f)
    f.close()

    #Set THERMOplate Scale to Farenheit
    THERMO.setSCALE('f')
    #Set our Start Time and next triggers for our SSRs
    startTime = round(time.time(), 1)

    #Turn on Heatsink Fans
    DAQC2.setDOUTbit(DP, 2)
    DAQC2.setDOUTbit(DP, 3)

    def GetHeatsink(channel):
        global DP
        corrected = 0
        try:
            raw = DAQC2.getADC(DP,channel)
            corrected = (raw * 505) / 10.24
        except:
            corrected = -1
        return round(corrected, 2)

    def GetCPU():
        cpu = CPUTemperature()
        return cpu.temperature

    def TurnHLTOn():
        global DP
        global data
        DAQC2.setDOUTbit(DP, 0)
        data['HltStatus'] = 1

    def TurnHLTOff():
        global DP
        global data
        DAQC2.clrDOUTbit(DP, 0)
        data['HltStatus'] = 0

    def TurnBKOn():
        global DP
        global data
        DAQC2.setDOUTbit(DP, 1)
        data['BkStatus'] = 1

    def TurnBKOff():
        global DP
        global data
        DAQC2.clrDOUTbit(DP, 1)
        data['BkStatus'] = 0

    while True:
        currTime = round(time.time(), 1)

        #Update existing values
        if UpdateTemps:
            #Load Data
            f = open('/var/www/html/py/data.json', 'r')
            data = json.load(f)
            f.close()

            #Update Data
            data['HltHsTemp'] = GetHeatsink(0)
            data['CpuTemp'] = GetCPU()
            data['BkHsTemp'] = GetHeatsink(1)
            data['HltTemp'] = THERMO.getTEMP(0,11)
            data['MtTemp'] = THERMO.getTEMP(0,10)
            data['BkTemp'] = THERMO.getTEMP(0,9)
            UpdateTemps = False

            #Update Uptime File
            f = open('/var/www/html/py/uptime', 'w')
            f.write(str(currTime - startTime))
            f.close()

        else:
            UpdateTemps = True

        #HLTControl
        if data['HltMode'] == 'A':
            HLTOn = ActionCount + 5
            if data['HltTemp'] < (data['HltAuto'] - data['HltDelta']):
                TurnHLTOn()
            else:
                TurnHLTOff()
        else:
            if HLTOn == ActionCount:
                TurnHLTOn()
                HLTOn = ActionCount + (data['HltCycle'] * 2)
                HLTOff = HLTOn - ((float(data['HltMan']) / 100) * (data['HltCycle'] * 2))
            if HLTOff == ActionCount:
                TurnHLTOff()
        
        #BKControl
        if data['BkMode'] == 'A':
            BKOn = ActionCount + 5
            if data['BkTemp'] < (data['BkAuto'] - data['BkDelta']):
                TurnBKOn()
            else:
                TurnBKOff()
        else:
            if BKOn == ActionCount:
                TurnBKOn()
                BKOn = ActionCount + (data['BkCycle'] * 2)
                BKOff= BKOn - ((float(data['BkMan']) / 100) * (data['BkCycle'] * 2))
            if BKOff == ActionCount:
                TurnBKOff()

        ActionCount += 1

        #Save Data
        f = open('/var/www/html/py/data.json', 'w')
        json.dump(data, f)
        f.close()

        #Sleep
        time.sleep(0.5)
except Exception as e:
    now = datetime.now()
    print(e)
    f = open('/var/www/html/python_errors.log', 'a')
    f.write("%s - AZURE - %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), e))
    f.close()