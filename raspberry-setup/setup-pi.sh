#!/bin/bash

# setup GIT
git config --global user.name "ben"
git config --global user.email "ben@alarmpi"

# remove unnecessary packages
sudo apt purge xserver* lightdm* raspberrypi-ui-mods vlc* lxde* chromium* desktop* \
                gnome* gstreamer* gtk* hicolor-icon-theme* lx* mesa* pulseaudio \
                bluez cups triggerhappy modemmanager
sudo apt autoremove

# install required packages
sudo apt install -y python3-pip \
                build-essential \
                python-dev \
                python3-dev \
                python3-rpi.gpio \
                python3-flask \
                nano nginx

# install required python modules
pip install pad4pi waitress

# some aliases
cat <<EOF > ~/.bash_aliases 
alias ll='ls -la'
alias l='ls -la'
EOF                

# configure and start nginx service
sudo systemctl enable nginx
sudo cat nginx.conf >> /etc/nginx/sites-available/default
sudo systemctl start nginx

# install systemd service 
sudo cp alarmpi.service /etc/systemd/system/
sudo systemctl enable alarmpi
sudo systemctl start alarmpi
