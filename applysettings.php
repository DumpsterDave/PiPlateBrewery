<?php
    try {
        $DATAFILE = './py/data.json';
        $Data = json_decode(file_get_contents($DATAFILE));
        $Data->{'HltCycle'} = intval($_GET['hltcycle'] ?? $Data->{'HltCycle'});
        $Data->{'HltDelta'} = floatval($_GET['hltdelta'] ?? $Data->{'HltDelta'});
        $Data->{'MtDelta'} = floatval($_GET['mtdelta'] ?? $Data->{'MtDelta'});
        $Data->{'BkCycle'} = intval($_GET['bkcycle'] ?? $Data->{'BkCycle'});
        $Data->{'BkDelta'} = floatval($_GET['bkdelta'] ?? $Data->{'BkDelta'});
        file_put_contents($DATAFILE, json_encode($Data));
    } catch (Exception $ex){
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - APPLY SETTINGS - " . $ex->getMessage());
        fclose($f);
    }
    
?>