#!/bin/bash
if [ -d /home/ubuntu/wagtail ]; then
    /home/ubuntu/wagtail/wagtail.docker.start.sh
    /home/ubuntu/wagtail/wagtail.start.sh
fi
