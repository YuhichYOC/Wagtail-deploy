#!/bin/bash
docker run --name wagtail \
    -p 8000:8000 \
    -d -i -t \
    [yuhichyoc/wagtail] \
    /bin/bash
