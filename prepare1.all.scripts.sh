#!/bin/bash
. ./common.sh
find ./ -name "*.sh" -type f | mod754
find ./ -name "*.sh" -type f | replace "\[/home/ubuntu\]"   ""
