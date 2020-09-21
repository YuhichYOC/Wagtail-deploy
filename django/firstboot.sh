#!/bin/bash
docker run --name django \
    -p 8880:80 \
    -p 8000:8000 \
    -d -i -t \
    [yuhichyoc/django] \
    /bin/bash
