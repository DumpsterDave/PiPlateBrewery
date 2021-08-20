<?php
    try {
        $Target = strtoupper($_GET['set']);
        $Mode = intval($_GET['mode']);
        if ($Mode == 1) {
            $Value = floatval($_GET['value']);
        } else {
            $Value = intval($_GET['value']);
        }
        $Arr = array("Target"=>$Target, "Mode"=>$Mode, "Value"=>$Value);
        file_put_contents('./py/temp.json', json_encode($Arr));
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - SET TEMP - " . $ex->getMessage());
        fclose($f);
    }
?>