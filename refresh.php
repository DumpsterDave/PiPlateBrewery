<?php
    try {
        $JSONRaw = file_get_contents('./py/data.json');
        $Data = json_decode($JSONRaw);
        $TcPID = file_get_contents('./py/tc.pid');
        if (strlen($TcPID) == 0) {
            $TcPID = 0;
        }
        $AzPID = file_get_contents('./py/az.pid');
        if (strlen($AzPID) == 0) {
            $AzPID = 0;
        }
        
        if ($Data->{'HltMode'} == 'A') {
            $HltSet = $Data->{'HltAuto'};
        } else {
            $HltSet = $Data->{'HltMan'};
        }
        if ($Data->{'BkMode'} == 'A') {
            $BkSet = $Data->{'BkAuto'};
        } else {
            $BkSet = $Data->{'BkMan'};
        }
        $Uptime = intval(file_get_contents('py/uptime'));
        $Hrs = floor($Uptime / 3600);
        $Min = floor($Uptime / 60 % 60);
        $Sec = floor($Uptime % 60);
        $Elapsed = sprintf('%02d:%02d:%02d', $Hrs, $Min, $Sec);
        echo "{$Data->{'HltHsTemp'}},{$Data->{'CpuTemp'}},{$Data->{'BkHsTemp'}},{$Data->{'HltTemp'}},{$HltSet},{$Data->{'MtTemp'}},{$Data->{'MtAuto'}},{$Data->{'BkTemp'}},{$BkSet},{$Data->{'HltMode'}},{$Data->{'BkMode'}},{$Elapsed},{$Data->{'HltCycle'}},{$Data->{'BkCycle'}},{$Data->{'HltDelta'}},{$Data->{'MtDelta'}},{$Data->{'BkDelta'}},{$TcPID},{$AzPID}";
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - REFRESH - " . $ex->getMessage());
        fclose($f);
    }
?>