<?php
    try {
        $action = strtolower($_GET['action']) ?? 0;
        $pid = intval($_GET['pid'] ?? 0);
        if ($action !== 0) {
            $ret = "";
            switch($action) {
                case "starttc":
                    //$cmd = escapeshellcmd('/usr/bin/python2.7 /var/www/html/py/tempcontrol.py & echo $! >/var/www/html/py/tc.pid');
                    $cmd = escapeshellcmd('/var/www/html/py/starttc.sh');
                    echo shell_exec($cmd);
                    break;
                case "stoptc":
                    $cmd = escapeshellcmd('sudo pkill -2 --pidfile /var/www/html/py/tc.pid');
                    shell_exec(sprintf("%s 2>&1 &", $cmd));
                    file_put_contents('/var/www/html/py/tc.pid', '0');
                    break;
                case "startla":
                    //$cmd = escapeshellcmd('/usr/bin/python2.7 /var/www/html/py/tempcontrol.py & echo $! >/var/www/html/py/tc.pid');
                    $cmd = escapeshellcmd('/var/www/html/py/startla.sh');
                    echo shell_exec($cmd);
                    break;
                case "stopla":
                    $cmd = escapeshellcmd('sudo pkill -2 --pidfile /var/www/html/py/az.pid');
                    shell_exec(sprintf("%s 2>&1 &", $cmd));
                    file_put_contents('/var/www/html/py/az.pid', '0');
                    break;
            }
        }
    } catch (Exception $ex) {
        $f = fopen('./php_error_log', 'w+');
        fwrite($f, date('Y-m-d H:i:s') . " - PYTHON - " . $ex->getMessage());
        fclose($f);
    }
?>