<?php
    try {
        $Target = strtoupper($_GET['set']);
        $Arr = array("Target"=>$Target, "NewMode"=>$_GET['mode']);
        file_put_contents('./py/mode.json', json_encode($Arr));
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - SET MODE - " . $ex->getMessage());
        fclose($f);
    }
?>