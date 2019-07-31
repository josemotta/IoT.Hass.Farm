#!/bin/bash
# set.sh

# Copy respective hass files to config folder
# Options are tank or super

E_NOARGS=75

if [ -z "$1" ]
then
  echo "Usage: `basename $0` [tank | super | pump]"
  exit $E_NOARGS
fi

case $1 in
  tank)
    cp -t . _tank/*.yaml
#    cp -t /etc/NetworkManager/system-connections _tank/bin/canoasystem
    ;;
  super)
    cp -t . _super/*.yaml
#    cp -t /etc/NetworkManager/system-connections _super/bin/wired
    ;;
  pump)
    cp -t . _pump/*.yaml
    cp -t ./custom_components/ _pump/bin/custom_components/
#    cp -t /etc/NetworkManager/system-connections _pump/bin/wired
    ;;
esac
