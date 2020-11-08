#!/bin/bash

DJANGO_START() {
  docker start django
  docker exec -d django /bin/bash -c '/etc/init.d/nginx start && cd /[django-name] && uwsgi --socket [django-name].sock --module [django-name].wsgi --chmod-socket=666'
}

WAGTAIL_START() {
  docker start wagtail
  docker exec -d wagtail /bin/bash -c '/etc/init.d/nginx start && cd /[wagtail-name] && uwsgi --socket [wagtail-name].sock --module [wagtail-name].wsgi --chmod-socket=666'
}

if [ -d /home/ubuntu/django ]; then
  DJANGO_START
fi
if [ -d /home/ubuntu/wagtail ]; then
  WAGTAIL_START
fi
