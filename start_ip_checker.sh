#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
cd /home/avsolatorio/WORK/utils/ip-change-notification

nohup stdbuf -oL python public_ip_checker.py > nohup.out &

