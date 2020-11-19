#!/bin/sh -e
/usr/bin/python2.7 /var/www/html/py/tempcontrol.py &
echo $! >/var/www/html/py/tc.pid
