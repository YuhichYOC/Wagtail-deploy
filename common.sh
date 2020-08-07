#!/bin/bash

mod754() {
  while read -r file
  do
    chmod 754 $file
  done
}

replace() {
  while read -r file
  do
    cat $file | sed -i -e "s/$1/$2/g" $file
  done
}
