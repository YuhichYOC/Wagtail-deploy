#!/bin/bash
. ./common.sh
find ./wagtail/ -name "*" -type f | replace "\[myproject\]"           ""
find ./ -name "*" -type f         | replace "\[yuhichyoc/wagtail\]"   ""
. ./wagtail/build.sh
. ./wagtail/firstboot.sh
