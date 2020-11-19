<?php
    try {
        $DATAFILE = './py/data.json';
        $Data = json_decode(file_get_contents($DATAFILE));
        $NewData = array("HltCycle"=>0, "HltDelta"=>0.0, "MtDelta"=>0.0, "BkCycle"=>0, "BkDelta"=>0.0);
        $NewData['HltCycle'] = intval($_GET['hltcycle'] ?? $Data->{'HltCycle'});
        $NewData['HltDelta'] = floatval($_GET['hltdelta'] ?? $Data->{'HltDelta'});
        $NewData['MtDelta'] = floatval($_GET['mtdelta'] ?? $Data->{'MtDelta'});
        $NewData['BkCycle'] = intval($_GET['bkcycle'] ?? $Data->{'BkCycle'});
        $NewData['BkDelta'] = floatval($_GET['bkdelta'] ?? $Data->{'BkDelta'});
        file_put_contents('./py/settings.json', json_encode($NewData));
    } catch (Exception $ex){
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - APPLY SETTINGS - " . $ex->getMessage());
        fclose($f);
    }
    
?>