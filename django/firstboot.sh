#!/bin/bash
docker run --name django \
    -p 8010:8010 \
    -p 8011:8011 \
    -p 8012:8012 \
    -p 8013:8013 \
    -p 8014:8014 \
    -p 8015:8015 \
    -d -i -t \
    yuhichyoc/django \
    /bin/bash
