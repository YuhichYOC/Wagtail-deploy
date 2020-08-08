#!/bin/bash

mod754() {
  while read -r file
  do
    chmod 754 $file
  done
}

randomsecretkey() {
  echo $(cat /dev/urandom | base64 | fold -w 50 | head -n 1 | sed -e 's|@|a|g')
}

replace() {
  while read -r file
  do
    cat $file | sed -i -e "s@$1@$2@g" $file
  done
}
