#!/bin/bash

DJANGO_STOP() {
  docker stop django
}

WAGTAIL_STOP() {
  docker stop wagtail
}

if [ -d /home/ubuntu/django ]; then
  DJANGO_STOP
fi
if [ -d /home/ubuntu/wagtail ]; then
  WAGTAIL_STOP
fi
