#!/bin/bash
# PATH=/home/avsolatorio/ml-ai/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
PATH=/mnt/Datastore/ubuntu-2016/home/avsolatorio/ml-ai/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
cd ~/ip-change-notification/src

nohup stdbuf -oL python public_ip_checker.py > nohup.out 2>&1 &

