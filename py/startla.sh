#!/bin/sh -e
/usr/bin/python2.7 /var/www/html/py/azure.py &
echo $! >/var/www/html/py/az.pid
