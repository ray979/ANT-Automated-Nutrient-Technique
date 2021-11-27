#!/bin/bash
#Setup bash script in progress

pip3 install spidev
pip3 install pyserial

#Install BCM2835-1.45 provide by Waveshare
#Can also install libraries from http://www.airspayce.com/mikem/bcm2835/
cp ./BCM2835/Bcm2835-1.45.tar.gz $HOME/Bcm2835-1.45.tar.gz
cd
cd Bcm2835-1.45
./configure
make
sudo make check
sudo make install


