#!/bin/bash
docker stop django
docker start django
docker exec -d django /bin/bash -c '/etc/init.d/nginx start && cd /[django-name] && uwsgi --socket [django-name].sock --module [django-name].wsgi --chmod-socket=666'

