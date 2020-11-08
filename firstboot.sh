#!/bin/bash

# use this for allocating names and ports to each containers.

FIRSTRUN_DJANGO() {
  docker run --name django -p 8880:80 -p 8000:8000 -d -i -t yuhichyoc/django /bin/bash
}

FIRSTRUN_WAGTAIL() {
  docker run --name wagtail -p 8881:80 -p 8001:8000 -d -i -t yuhichyoc/django /bin/bash
}

if [ -d /home/ubuntu/django ]; then
  FIRSTRUN_DJANGO
fi
if [ -d /home/ubuntu/wagtail ]; then
  FIRSTRUN_WAGTAIL
fi
