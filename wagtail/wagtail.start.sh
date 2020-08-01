#!/bin/bash
docker exec -d wagtail python3 ./[myproject]/manage.py runserver 0.0.0.0:8000
