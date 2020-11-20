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
        $Data->{"TcPID"} = $TcPID;
        $Data->{"LaPID"} = $AzPID;
        $Uptime = intval(file_get_contents('py/uptime'));
        $Hrs = floor($Uptime / 3600);
        $Min = floor($Uptime / 60 % 60);
        $Sec = floor($Uptime % 60);
        $Elapsed = sprintf('%02d:%02d:%02d', $Hrs, $Min, $Sec);
        $Data->{"Elapsed"} = $Elapsed;
        $JSON = json_encode($Data);
        echo $JSON;    
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - REFRESH - " . $ex->getMessage());
        fclose($f);
    }
?>