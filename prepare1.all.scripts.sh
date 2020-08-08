#!/bin/bash
. ./common.sh
find ./ -name "*.sh" -type f | mod754
find ./ -name "*.sh" -type f | replace "\[/home/ubuntu/\]"       $(pwd)"/"
find ./ -name "*" -type f    | replace "\[yuhichyoc/wagtail\]"   ""
find ./ -name "*" -type f    | replace "\[yuhichyoc/django\]"    ""
