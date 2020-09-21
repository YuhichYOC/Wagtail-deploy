#!/bin/bash
docker exec -d django-test /bin/bash -c '/etc/init.d/nginx start && cd /[project-name] && uwsgi --socket [project-name].sock --module [project-name].wsgi --chmod-socket=666'
