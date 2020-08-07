#!/bin/bash
. ./common.sh
find ./django/ -name "*" -type f | replace "\[django-project\]"              ""
find ./django/ -name "*" -type f | replace "\[app\]"                         ""
find ./django/ -name "*" -type f | replace "\[host ip address\]"             ""
find ./django/ -name "*" -type f | replace "\[django-project secret key\]"   ""
find ./ -name "*" -type f        | replace "\[yuhichyoc/django\]"            ""
. ./django/build.sh
. ./django/firstboot.sh
