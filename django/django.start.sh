#!/bin/bash
docker exec -d django python3 ./[django-project]/manage.py runserver 0.0.0.0:8010
