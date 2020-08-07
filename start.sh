#!/bin/bash
if [ -d [/home/ubuntu/]wagtail ]; then
    [/home/ubuntu/]wagtail/wagtail.docker.start.sh
    [/home/ubuntu/]wagtail/wagtail.start.sh
fi
if [ -d [/home/ubuntu/]django ]; then
    [/home/ubuntu/]django/django.docker.start.sh
    [/home/ubuntu/]django/django.start.sh
fi
