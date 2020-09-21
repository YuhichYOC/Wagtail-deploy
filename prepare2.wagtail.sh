#!/bin/bash
. ./common.sh
find ./wagtail/ -name "*" -type f | replace "\[project-name\]"   ""
TEST_VALUE=$(docker images | awk '("[yuhichyoc/wagtail]" == $1) {print $1}' | wc -l)
if [ 0 -eq $TEST_VALUE ]; then
  cd [/home/ubuntu/]wagtail
  . ./build.sh
  . ./firstboot.sh
fi
