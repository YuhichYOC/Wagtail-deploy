#!/bin/bash
docker run --name wagtail \
    -p 8881:80 \
    -p 8001:8000 \
    -d -i -t \
    [yuhichyoc/wagtail] \
    /bin/bash
