#!/usr/bin/python
import piplates.THERMOplate as THERMO
import piplates.DAQC2plate as DAQC2
from gpiozero import CPUTemperature
from datetime import datetime
import time
import math
import json
import os
import sys
import signal

run = True

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

    def OnKill(signum, frame):
        global run, DP
        run = False
        TurnHLTOff()
        TurnBKOff()
        DAQC2.clrDOUTbit(DP, 2)
        DAQC2.clrDOUTbit(DP, 3)

    signal.signal(signal.SIGINT, OnKill)
    signal.signal(signal.SIGTERM, OnKill)

    while run:
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

            #Check for Updated Targets
                #Mode
            if os.path.exists('/var/www/html/py/mode.json'):
                f = open('/var/www/html/py/mode.json', 'r')
                NewData = json.load(f)
                f.close()
                if NewData['Target'] == 'hlt':
                    data['HltMode'] = NewData['NewMode']
                elif NewData['Target'] == 'bk':
                    data['BkMode'] = NewData['NewMode']
                os.remove('/var/www/html/py/mode.json')

                #Temp
            if os.path.exists('/var/www/html/py/temp.json'):
                f = open('/var/www/html/py/temp.json', 'r')
                NewData = json.load(f)
                f.close()
                if NewData['Target'] == 'hlt' and NewData['Mode'] == 'a':
                    data['HltAuto'] = NewData['Value']
                elif NewData['Target'] == 'hlt' and NewData['Mode'] == 'm':
                    data['HltMan'] = NewData['Value']
                elif NewData['Target'] == 'mt' and NewData['Mode'] == 'a':
                    data['MtAuto'] = NewData['Value']
                elif NewData['Target'] == 'bk' and NewData['Mode'] == 'a':
                    data['BkAuto'] = NewData['Value']
                elif NewData['Target'] == 'bk' and NewData['Mode'] == 'm':
                    data['BkMan'] = NewData['Value']
                os.remove('/var/www/html/py/temp.json')

                #Settings
            if os.path.exists('/var/www/html/py/settings.json'):
                f = open('/var/www/html/py/settings.json', 'r')
                NewData = json.load(f)
                f.close()
                data['HltCycle'] = NewData['HltCycle']
                data['HltDelta'] = NewData['HltDelta']
                data['MtDelta'] = NewData['MtDelta']
                data['BkCycle'] = NewData['BkCycle']
                data['BkDelta'] = NewData['BkDelta']
                os.remove('/var/www/html/py/settings.json')

        else:
            UpdateTemps = True

        #HLTControl
        if data['HltMode'] == 'A':
            HLTOn = ActionCount + 1
            if data['HltTemp'] < (data['HltAuto'] - data['HltDelta']):
                TurnHLTOn()
            else:
                TurnHLTOff()
        else:
            if HLTOn == ActionCount:
                TurnHLTOn()
                HltCycleLen = data['HltCycle'] * 2
                HLTOn = ActionCount + HltCycleLen
                HLTOff = ActionCount + ((float(data['HltMan']) / 100) * HltCycleLen)
            if HLTOff == ActionCount:
                TurnHLTOff()
            elif HLTOn < ActionCount and HLTOff < ActionCount:
                HLTOn = ActionCount + 1
        
        #BKControl
        if data['BkMode'] == 'A':
            BKOn = ActionCount + 1
            if data['BkTemp'] < (data['BkAuto'] - data['BkDelta']):
                TurnBKOn()
            else:
                TurnBKOff()
        else:
            if BKOn == ActionCount:
                TurnBKOn()
                BkCycleLen = data['BkCycle'] * 2
                BKOn = ActionCount + BkCycleLen
                BKOff = ActionCount + ((float(data['BkMan']) / 100) * BkCycleLen)
            if BKOff == ActionCount:
                TurnBKOff()
            elif BKOn < ActionCount and BKOff < ActionCount:
                BKOn = ActionCount + 1

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
    f.write("%s - TEMP CONTROL [%i] - %s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), sys.exc_info()[-1].tb_lineno, e))
    f.close()

now = datetime.now()
f = open('/var/www/html/python_errors.log', 'a')
f.write("%s - TEMP CONTROL [0] - Exit called from interface\n" % (now.strftime("%Y-%m-%d %H:%M:%S")))
f.close()