#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
cd ~/ip-change-notification/src

nohup stdbuf -oL python public_ip_checker.py > nohup.out 2>&1 &

