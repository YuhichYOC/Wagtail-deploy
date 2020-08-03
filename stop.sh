#!/bin/bash
if [ -d /home/ubuntu/wagtail ]; then
    /home/ubuntu/wagtail/wagtail.docker.stop.sh
fi
if [ -d /home/ubuntu/django ]; then
    /home/ubuntu/django/django.docker.stop.sh
fi
