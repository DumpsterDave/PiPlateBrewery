<?php
    #Perform Initial Data Load
    try {
        //Perform Initial Data Load
        $Data = json_decode(file_get_contents('./py/data.json'));

        //Verify Process ID Files Exist or create them
        if (!file_exists('./py/tc.pid')) {
            file_put_contents('./py/tc.pid', '0');
        }
        if (!file_exists('./py/az.pid')) {
            file_put_contents('./py/az.pid', '0');
        }
?>
<html>
    <head>
        <!--
            All code and artwork (C) 2020 Scott Corio except:

            Restart Icon by Frank Souza
            https://www.iconfinder.com/iconsets/fs-icons-ubuntu-by-franksouza-

            Power Icon by Artyom Khamitov
            https://www.iconfinder.com/iconsets/glyphs

            Up/Down Icons by Vathanx
            https://www.iconfinder.com/iconsets/ionicons

            Gear Icon by Assyifa Art
            https://www.iconfinder.com/iconsets/user-interface-glyph-5

            Thermometer Icon by Yannick Lung
            https://www.iconfinder.com/iconsets/hawcons

        -->
        <script src="brew.js"></script>
        <link rel="stylesheet" href="brew.css">
    </head>
    <body onLoad="InitializeTimers();">
        <div id="Main">
            <div id="HltHsContainer" class="TempOk">
                <table width="384" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="Label">HLT</td><td id="HltHsTemp" class="Temp"><?php echo round($Data->{'HLT'}->{'HsTemp'}, 1); ?>&#8451;</td>
                    </tr>
                </table>
            </div>
            <div id="EncContainer" class="TempWarn">
                <table width="384" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="Label">CPU</td><td id="EncTemp" class="Temp"><?php echo round($Data->{'CPU'}->{'HsTemp'}, 1); ?>&#8451;</td>
                    </tr>
                </table>
            </div>
            <div id="BkHsContainer" class="TempHigh">
                <table width="384" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="Label">BK</td><td id="BkHsTemp" class="Temp"><?php echo round($Data->{'BK'}->{'HsTemp'}, 1); ?>&#8451;</td>
                    </tr>
                </table>
            </div>
            <div id="HltContainer">
            <div id="HltTemp" class="TempLow" onClick="ShowSetTarget('hlt');">
                    <div class="TunLabel">Sv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="HltTempSet"><?php echo round($Data->{'HLT'}->{'sv'}, 1); ?>&#8457;</span>
                    <div class="TunLabel">Pv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="HltTempValue"><?php echo round($Data->{'HLT'}->{'pv'}, 1); ?>&#8457;</span>
                </div>
                <a id="HltModeLink" href="#" onClick="ChangeMode('HLT',0);"><div id="HltMode" class="ModeAuto">AUTO</div></a>
            </div>
            <div id="MtContainer">
                <div id="MtTemp" class="TempOk" onClick="ShowSetTarget('mt');">
                    <div class="TunLabel">Sv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="MtTempSet"><?php echo round($Data->{'MT'}->{'sv'}, 1); ?>&#8457;</span>
                    <div class="TunLabel">Pv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="MtTempValue"><?php echo round($Data->{'MT'}->{'pv'}, 1); ?>&#8457;</span>
                </div>
            </div>
            <div id="BkContainer">
                <div id="BkTemp" class="TempHigh" onClick="ShowSetTarget('bk');">
                    <div class="TunLabel">Sv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="BkTempSet"><?php echo round($Data->{'BK'}->{'sv'}, 1); ?>&#8457;</span>
                    <div class="TunLabel">Pv:&nbsp;&nbsp;</div>
                    <span class="TunTemp" id="BkTempValue"><?php echo round($Data->{'BK'}->{'pv'}, 1); ?>&#8457;</span>
                </div>
                <a id="BkModeLink" href="#" onClick="ChangeMode('BK',1);"><div id="BkMode" class="ModeMan">MAN</div></a>
            </div>
            <div class="PidOutputContainer" id="HltPidOutput">
                <div class="PidOutputBar" id="HltPidOutputBar"></div>
                <div class="PidOutputValue" id="HltPidOutputValue">50</div>
            </div>
            <div class="PidOutputContainer" id="MtpH">
                <div class="PidOutputBar" id="MtpHBar"></div>
                <div class="PidOutputValue" id="MtpHValue">7</div>
            </div>
            <div class="PidOutputContainer" id="BkPidOutput">
                <div class="PidOutputBar" id="BkPidOutputBar"></div>
                <div class="PidOutputValue" id="BkPidOutputValue">50</div>
            </div>
            <div id="Runtime"><b>Runtime:&nbsp;&nbsp;</b><span id="TimeElapsed">00:00:00</span></div>
            <div id="Refresh" onClick="window.location.reload(true);"><img src="img/refresh.png"/></div>
            <div id="Azure" onClick="ToggleLogAnalytics();"><img id="lastatus" src="img/la_off.png"/><input type="hidden" id="lapid" value=""/></div>
            <div id="TempC" onClick="ToggleTempControl();"><img id="tempcstatus" src="img/tempc_off.png"/><input type="hidden" id="tcpid" value=""/></div>
            <div id="Config" onClick="ShowSettings();"><img src="img/config.png" alt="Config" /></div>
        </div>
        <div id="SetTarget">
            <div id="SetTargetButtons">
                <div class="SetButton" onClick="SetButtonClick('1');">1</div>
                <div class="SetButton" onClick="SetButtonClick('2');">2</div>
                <div class="SetButton" onClick="SetButtonClick('3');">3</div>
                <div class="SetButton" onClick="SetButtonClick('4');">4</div>
                
                <div class="SetButton" onClick="SetButtonClick('5');">5</div>
                <div class="SetButton" onClick="SetButtonClick('6');">6</div>
                <div class="SetButton" onClick="SetButtonClick('7');">7</div>
                <div class="SetButton" onClick="SetButtonClick('8');">8</div>

                <div class="SetButton" onClick="SetButtonClick('9');">9</div>
                <div class="SetButton" onClick="SetButtonClick('0');">0</div>
                <div class="SetButtonDouble"style="border-color: #00a2e8; color: #00a2e8;"  onClick="SetButtonClick('D');">DEL</div>

                <div class="SetButton" style="border-color: #fff200; color: #fff200;" onClick="ClearNewTarget();">C</div>
                <div class="SetButton" style="border-color: #ed1c24; color: #ed1c24;" onClick="HideSetTarget();">X</div>
                <div class="SetButtonDouble" style="border-color: #22b14c; color: #22b14c;" onClick="SetNewTemp();">OK</div>
                <input type="hidden" id="SetTargetCaller" value="" />
            </div>
            <div id="SetTargetValues">
               <div class="SetTargetLabel">New Value:</div>
               <div class="SetTargetValue" id="SetTargetValueNew">999.9</div>
               <div class="SetTargetLabel">Current Value:</div>
               <div class="SetTargetValue" id="SetTargetValueCurrent">999.9</div>
            </div>
        </div>
        <div id="Settings">
            <div id="SettingsGrid">
                <!-- Captions -->
                <div></div>
                <div></div>
                <div class="SettingsHeader">Cycle Time (s)</div>
                <div></div>
                <div class="SettingsHeader">Delta</div>
                <div></div>

                <!-- HLT -->
                <div class="SettingsLabel">HLT</div>
                <div class="SettingsText"></div>
                <div class="SettingsText" id="hltcycle">10</div>
                <div class="SettingsUpDown"><img src="img/inc.png" onClick="AlterSetting('hlt', 'cycle', 'inc');"/></div>
                <div class="SettingsText" id="hltdelta">2</div>
                <div class="SettingsUpDown"><img src="img/inc.png" onClick="AlterSetting('hlt', 'delta', 'inc');"/></div>

                <div class="SettingsUpDown"><img src="img/dec.png" onClick="AlterSetting('hlt', 'cycle', 'dec');"/></div>
                <div class="SettingsUpDown"><img src="img/dec.png" onClick="AlterSetting('hlt', 'delta', 'dec');"/></div>
                <!-- MT -->
                <div class="SettingsLabel">MT</div>
                <div class="SettingsText"></div>
                <div class="SettingsText"></div>
                <div class="SettingsUpDown"></div>
                <div class="SettingsText" id="mtdelta">2</div>
                <div class="SettingsUpDown"><img src="img/inc.png" onClick="AlterSetting('mt', 'delta', 'inc');"/></div>

                <div class="SettingsUpDown"></div>
                <div class="SettingsUpDown"><img src="img/dec.png"  onClick="AlterSetting('mt', 'delta', 'dec');"/></div>

                <!-- BK -->
                <div class="SettingsLabel">BK</div>
                <div class="SettingsText"></div>
                <div class="SettingsText" id="bkcycle">10</div>
                <div class="SettingsUpDown"><img src="img/inc.png"  onClick="AlterSetting('bk', 'cycle', 'inc');"/></div>
                <div class="SettingsText" id="bkdelta">2</div>
                <div class="SettingsUpDown"><img src="img/inc.png"  onClick="AlterSetting('bk', 'delta', 'inc');"/></div>

                <div class="SettingsUpDown"><img src="img/dec.png" onClick="AlterSetting('bk', 'cycle', 'dec');"/></div>
                <div class="SettingsUpDown"><img src="img/dec.png" onClick="AlterSetting('bk', 'delta', 'dec');"/></div>
            </div>
            <div class="SettingsButton" style="right: 920px; color: #ed1c24; border-color: #ed1c24;" onClick="Power('off');"><img src="img/power.png"/></div>
            <div class="SettingsButton" style="right: 648px; color: #ff7f27; border-color: #ff7f27;" onClick="Power('reset');"><img src="img/restart.png"/></div>
            <div class="SettingsButton" style="left: 648px; color: #fff200; border-color: #fff200;" onClick="HideSettings();">X</div>
            <div class="SettingsButton" style="left: 920px; color: #22b14c; border-color: #22b14c;" onClick="SaveSettings();">OK</div>
        </div>
    </body>
</html>
<?php
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - INDEX - " . $ex->getMessage());
        fclose($f);
    }
?>