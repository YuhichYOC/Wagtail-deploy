#!/bin/bash
REBOOT_LOGFILE="/home/ubuntu/reboot.log"
TEST_VALUE=$(docker ps | wc -l)
if [ $TEST_VALUE -eq 1 ]; then
    echo "`date "+%Y-%m-%d %H:%M:%S"` system will going to restart" | tee -a $REBOOT_LOGFILE
    /sbin/shutdown -r now
else
    echo "`date "+%Y-%m-%d %H:%M:%S"` any container are still alive, reboot canceled" | tee -a $REBOOT_LOGFILE
fi
