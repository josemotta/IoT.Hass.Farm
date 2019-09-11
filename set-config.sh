#!/bin/bash
# set.sh

# Copy respective hass files to config folder
# Options are tank | super | pump
# Use nmcli interactive connection editor to set each node IP
# TODO: - Auto config network manager for all nodes

E_NOARGS=75

NM="/etc/NetworkManager/system-connections"

if [ -z "$1" ]
then
  echo "Usage: `basename $0` [tank | super | pump]"
  exit $E_NOARGS
fi

case $1 in
  tank)
    cp -t . _tank/*.yaml
    # if [ -d "$NM" ]; then
    #   # Copy network manager configuration
    #   cp -t /etc/NetworkManager/system-connections _tank/bin/canoasystem
    # fi
    ;;
  super)
    cp -t . _super/*.yaml
    # if [ -d "$NM" ]; then
    #   # Copy network manager configuration
    #   cp -t /etc/NetworkManager/system-connections _super/bin/wired
    # fi
    ;;
  pump)
    cp -t . _pump/*.yaml
    cp -r _pump/bin/custom_components .
    # if [ -d "$NM" ]; then
    #   # Copy network manager configuration
    #   cp -t /etc/NetworkManager/system-connections _pump/bin/wired
    # fi
    ;;
esac
## Set UI language
if [ $# -eq 2 ]
then
  mv ui-lovelace-$2.yaml ui-lovelace.yaml
fi

