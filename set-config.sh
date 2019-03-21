#!/bin/bash
# set.sh

# Copy respective hass files to config folder
# Options are castle or super

E_NOARGS=75

if [ -z "$1" ]
then
  echo "Usage: `basename $0` [castle | super]"
  exit $E_NOARGS
fi

case $1 in
  castle)
    cp -t . _castle/*
    ;;
  super)
    cp -t . _super/*
    ;;
esac
