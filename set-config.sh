#!/bin/bash
# set.sh

# Copy respective hass files to config folder
# Options are tank or super

E_NOARGS=75

if [ -z "$1" ]
then
  echo "Usage: `basename $0` [tank | super]"
  exit $E_NOARGS
fi

case $1 in
  tank)
    cp -t . _tank/*
    ;;
  super)
    cp -t . _super/*
    ;;
esac
