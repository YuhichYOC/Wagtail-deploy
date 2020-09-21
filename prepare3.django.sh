#!/bin/bash
. ./common.sh
find ./django/ -name "*" -type f | replace "\[project-name\]"              ""
find ./django/ -name "*" -type f | replace "\[app\]"                         ""
find ./django/ -name "*" -type f | replace "\[host ip address\]"             ""
find ./django/ -name "*" -type f | replace "\[django-project secret key\]"   $(randomsecretkey)
TEST_VALUE=$(docker images | awk '("[yuhichyoc/django]" == $1) {print $1}' | wc -l)
if [ 0 -eq $TEST_VALUE ]; then
  cd [/home/ubuntu/]django
  . ./build.sh
  . ./firstboot.sh
fi
