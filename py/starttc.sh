#!/bin/sh -e
python3 /var/www/html/py/tempcontrol.py &
echo $! >/var/www/html/py/tc.pid
