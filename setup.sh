#! /bin/bash

echo "PiRadio Setup"

apt update
curl -sS get.pimoroni.com/onoffshim | bash
curl -sS get.pimoroni.com/phatbeat | bash
apt install -y vlc-nox
