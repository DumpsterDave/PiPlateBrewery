var SetTarget = 0;
var HLTHeatsink = 0;
var CPU = 0;
var BKHeatsink = 0;
var HLTSv = 0;
var HLTPv = 0;
var HLTMode = 'A';
var MTSv = 0;
var MTPv = 0;
var BKSv = 0;
var BKPv = 0;
var BKMode = 'A';
var InputMode = 'A';
var HltCycle, BkCycle;
var HltDelta, MtDelta, BkDelta;
var TcPID, LaPID;

function InitializeTimers() {
    setInterval(RefreshElements, 1000);
}

function RefreshElements() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var Values = JSON.parse(this.responseText);
            var v = 0;
            var s = 0;
            var tempState = "TempOk";

            //Process Time Elapsed
            document.getElementById("TimeElapsed").innerHTML = Values["Elapsed"];

            //Process Cycle Times
            HltCycle = Values["HltCycle"];
            BkCycle = Values["BkCycle"];

            //Process Deltas
            HltDelta = Values["HltDelta"];
            MtDelta = Values["MtDelta"];
            BkDelta = Values["BkDelta"];

            //Process PIDs
            TcPID = Values["TcPID"];
            LaPID = Values["LaPID"];

            //Process HLT Heatsink (Celcius)
            HLTHeatsink =Values["HltHsTemp"];
            if (HLTHeatsink >= 80) {
                tempState = "TempHigh";
            } else if (HLTHeatsink >= 70) {
                tempState = "TempWarn"
            }
            document.getElementById("HltHsTemp").innerHTML = HLTHeatsink.toFixed(1) + "&#8451;";
            document.getElementById("HltHsContainer").className = tempState;

            //Process CPU Temp (Celcius)
            tempState = "TempOk";
            CPU = Values["CpuTemp"];
            if (CPU >= 75) {
                tempState = "TempHigh";
            } else if (CPU >= 65) {
                tempState = "TempWarn"
            }
            document.getElementById("EncTemp").innerHTML = CPU.toFixed(1) + "&#8451;";
            document.getElementById("EncContainer").className = tempState;

            //Process BK Heatsink (Celcius)
            tempState = "TempOk";
            BKHeatsink = Values["BkHsTemp"];
            if (BKHeatsink >= 80) {
                tempState = "TempHigh";
            } else if (BKHeatsink >= 70) {
                tempState = "TempWarn"
            }
            document.getElementById("BkHsTemp").innerHTML = BKHeatsink.toFixed(1) + "&#8451;";
            document.getElementById("BkHsContainer").className = tempState;

            //Process HLT Temp
            tempState = "TempOk";
            HLTPv = Values["HltTemp"];
            if (Values["HltMode"] == 'A') {
                HltMode = 'A';
                HLTSv = Values["HltAuto"];
                if (HLTPv < (HLTSv - HltDelta)) {
                    tempState = "TempLow";
                } else if (HLTPv > (HLTSv + HltDelta)) {
                    tempState = "TempHigh";
                }
                document.getElementById("HltTempSet").innerHTML = HLTSv.toFixed(1) + "&#8457;";
                document.getElementById("HltMode").className = "ModeAuto";
                document.getElementById("HltMode").innerHTML = "AUTO";
                document.getElementById("HltModeLink").onclick = function(){ChangeMode('hlt','M');}
            } else {
                HltMode = 'M';
                HLTSv = Values["HltMan"];
                tempState = "TempMan";
                document.getElementById("HltTempSet").innerHTML = HLTSv.toFixed(0) + "%";
                document.getElementById("HltMode").className = "ModeMan";
                document.getElementById("HltMode").innerHTML = "MAN";
                document.getElementById("HltModeLink").onclick = function(){ChangeMode('hlt','A');}
            }
            document.getElementById("HltTempValue").innerHTML = HLTPv.toFixed(1) + "&#8457;";
            document.getElementById("HltTemp").className = tempState;

            //Process Mash Temp
            tempState = "TempOk";
            MTPv = Values["MtTemp"];
            MTSv = Values["MtAuto"];
            if (MTPv < (MTSv - MtDelta)) {
                tempState = "TempLow";
            } else if (MTPv > (MTSv + MtDelta)) {
                tempState = "TempHigh";
            }
            document.getElementById("MtTempSet").innerHTML = MTSv.toFixed(1) + "&#8457;";
            document.getElementById("MtTempValue").innerHTML = MTPv.toFixed(1) + "&#8457;";
            document.getElementById("MtTemp").className = tempState;

            //Process BK Temp
            tempState = "TempOk";
            BKPv = Values["BkTemp"];
            if (Values["BkMode"] == 'A') {
                BKMode = 'A';
                BKSv = Values["BkAuto"];
                if (BKPv < (BKSv - BkDelta)) {
                    tempState = "TempLow";
                } else if (BKPv > (BKSv + BkDelta)) {
                    tempState = "TempHigh";
                }
                document.getElementById("BkTempSet").innerHTML = BKSv.toFixed(1) + "&#8457;";
                document.getElementById("BkMode").className = "ModeAuto";
                document.getElementById("BkMode").innerHTML = "AUTO";
                document.getElementById("BkModeLink").onclick = function(){ChangeMode('bk','M');}
            } else {
                BKMode = 'M';
                BKSv = Values["BkMan"];
                tempState = "TempMan";
                document.getElementById("BkTempSet").innerHTML = BKSv.toFixed(0) + "%";
                document.getElementById("BkMode").className = "ModeMan";
                document.getElementById("BkMode").innerHTML = "MAN";
                document.getElementById("BkModeLink").onclick = function(){ChangeMode('bk','A');}
            }
            document.getElementById("BkTempValue").innerHTML = BKPv.toFixed(1) + "&#8457;";
            document.getElementById("BkTemp").className = tempState;       
        }
        document.getElementById('tcpid').value = TcPID;
        if ((TcPID !== null) && (TcPID > 0)) {
            document.getElementById('tempcstatus').src = 'img/tempc_on.png';
        } else {
            document.getElementById('tempcstatus').src = 'img/tempc_off.png';
        }

        document.getElementById('lapid').value = LaPID;
        if ((LaPID !== null) && (LaPID > 0)) {
            document.getElementById('lastatus').src = 'img/la_on.png';
        } else {
            document.getElementById('lastatus').src = 'img/la_off.png';
        }
    };
    xhttp.open("GET", "refresh.php", true);
    xhttp.send();
}

function ChangeMode(target, mode) {
    if ((target !== 'hlt') && (target !== "bk")) {
        return;
    }
    if ((mode !=="A") && (mode !== "M")) {
        return
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "setmode.php?set=" + target + "&mode=" + mode);
    xhttp.send();
}

function SetButtonClick(button) {
    var Temp = document.getElementById("SetTargetValueNew").innerHTML.replace(/\./g, '');
    var MaxL = 0;
    if (InputMode == "A") {
        MaxL = 4;
    } else {
        MaxL = 3
    }

    if (Temp.length <= MaxL) {
        if ((button == 'D') && (Temp.length > 1)) {
            Temp = Temp.substr(0, Temp.length - 1);
        } else if (button == 'D') {
            Temp = "";
        } else {
            if (Temp.length < MaxL) {
                Temp = Temp + button;
            }
        }
    }

    if (Temp.length !== 0) {
        if (InputMode == 'A') {
                document.getElementById("SetTargetValueNew").innerHTML = (parseFloat(Temp) / 10).toFixed(1);
        } else {
            var t = parseInt(Temp);
            if (t > 100) {
                t = 100;
            }
            document.getElementById("SetTargetValueNew").innerHTML = t;
        }
    } else {
        document.getElementById("SetTargetValueNew").innerHTML = "";
    }
}

function ClearNewTarget() {
    document.getElementById("SetTargetValueNew").innerHTML = "";
}

function HideSetTarget() {
    document.getElementById("SetTarget").style.visibility = "hidden";
}

function ShowSetTarget(caller) {
    document.getElementById("SetTarget").style.visibility = "visible";
    switch (caller) {
        case "hlt":
            ClearNewTarget();
            document.getElementById("SetTargetValueCurrent").innerHTML = HLTSv;
            document.getElementById("SetTargetCaller").value = caller;
            InputMode = HLTMode;
            break;
        case "mt":
            ClearNewTarget();
            document.getElementById("SetTargetValueCurrent").innerHTML = MTSv;
            document.getElementById("SetTargetCaller").value = caller;
            InputMode = "A";
            break;
        case "bk":
            ClearNewTarget();
            document.getElementById("SetTargetValueCurrent").innerHTML = BKSv;
            document.getElementById("SetTargetCaller").value = caller;
            InputMode = BKMode;
            break;
    }
}

function SetNewTemp() {
    if (document.getElementById("SetTargetValueNew").innerHTML.length !== 0) {

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                HideSetTarget();
            }
        };
        xhttp.open("GET", "settemp.php?set=" + document.getElementById("SetTargetCaller").value + "&value=" + document.getElementById("SetTargetValueNew").innerHTML + "&mode=" + InputMode);
        xhttp.send();
    }
}

function ShowSettings() {
    document.getElementById('hltcycle').innerHTML = HltCycle;
    document.getElementById('bkcycle').innerHTML = BkCycle;
    document.getElementById('hltdelta').innerHTML = HltDelta;
    document.getElementById('mtdelta').innerHTML = MtDelta;
    document.getElementById('bkdelta').innerHTML = BkDelta;
    document.getElementById("Settings").style.visibility = "visible";
}

function HideSettings() {
    document.getElementById("Settings").style.visibility = "hidden";
}

function AlterSetting(vessel, setting, dir) {
    var CurrentVal = parseFloat(document.getElementById(vessel + setting).innerHTML);
    var max, min, inc, dp;
    if (setting == 'cycle') {
        max = 30;
        min = 1;
        inc = 1;
        dp = 0;
    } else if (setting == 'delta') {
        max = 5;
        min = .2;
        inc = .1;
        dp = 1;
    }
    
    if (dir == 'inc') {
        CurrentVal += inc;
    } else {
        CurrentVal -= inc;
    }

    if (CurrentVal > max) {
        CurrentVal = max;
    }

    if (CurrentVal < min) {
        CurrentVal = min;
    }

    document.getElementById(vessel + setting).innerHTML = CurrentVal.toFixed(dp);
}

function SaveSettings() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            HideSettings();
        }
    };
    xhttp.open("GET", "applysettings.php?hltcycle=" + document.getElementById("hltcycle").innerHTML + "&hltdelta=" + document.getElementById("hltdelta").innerHTML + "&mtdelta=" + document.getElementById("mtdelta").innerHTML + "&bkcycle=" + document.getElementById("bkcycle").innerHTML + "&bkdelta=" + document.getElementById("bkdelta").innerHTML);
    xhttp.send();
}

function Power(action) {
    action = action.toLowerCase();
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "power.php?action=" + action, true);
    xhttp.send();
}

function ToggleTempControl() {
    if ((null == TcPID) || (TcPID <= 0)) {
        //PID is empty, TC must be off, turn it on
        document.getElementById('tempcstatus').src = 'img/tempc_on.png';
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById('tcpid').value = this.responseText;
            }
        };
        xhttp.open("GET", "python.php?action=starttc");
        xhttp.send();
    } else {
        document.getElementById('tempcstatus').src = 'img/tempc_off.png'
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById('tcpid').value = this.responseText;
            }
        };
        xhttp.open("GET", "python.php?action=stoptc");
        xhttp.send();
    }
}

function ToggleLogAnalytics() {
    if ((null == LaPID) || (LaPID <= 0)) {
        //PID is empty, LogAnlytics must be off, turn it on
        document.getElementById('lastatus').src = 'img/la_on.png';
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById('lapid').value = this.responseText;
            }
        };
        xhttp.open("GET", "python.php?action=startla");
        xhttp.send();
    } else {
        document.getElementById('lastatus').src = 'img/la_off.png'
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById('lapid').value = this.responseText;
            }
        };
        xhttp.open("GET", "python.php?action=stopla");
        xhttp.send();
    }
}