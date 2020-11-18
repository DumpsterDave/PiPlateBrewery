<?php
    try {
        $DATAFILE = './py/data.json';
        $Data = json_decode(file_get_contents($DATAFILE));
        $Target = ucwords($_GET['set']);
        $Mode = strtolower($_GET['mode']);
        $Value;
        if ($Mode == 'a') {
            $Target .= "Auto";
            $Value = floatval($_GET['value']);
        } else {
            $Target .= "Man";
            $Value = intval($_GET['value']);
        }
        $Data->{$Target} = $Value;
        file_put_contents($DATAFILE, json_encode($Data));
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - SET TEMP - " . $ex->getMessage());
        fclose($f);
    }
?>