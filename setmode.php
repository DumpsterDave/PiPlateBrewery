<?php
    try {
        $DATAFILE = './py/data.json';
        $Data = json_decode(file_get_contents($DATAFILE));
        $Target = ucwords($_GET['set']) . "Mode";
        $Data->{$Target} = $_GET['mode'] ?? 'A';
        
        file_put_contents($DATAFILE, json_encode($Data));
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - SET MODE - " . $ex->getMessage());
        fclose($f);
    }
?>