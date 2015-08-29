.. _install:

Installing and configuring Air Piano
====================================

Requirements
------------
Raspberry Pi Model B or Raspberry Pi 2 Model B
SD Card (you can check recomend SD card size an type at https://www.raspberrypi.org/documentation/installation/sd-cards.md)
Camera Module (https://www.raspberrypi.org/products/camera-module/)
HDMI cable and USB charger

Optional: wireless keyboard


Hardware configuration
----------------------

Install the camera module -> reference.
When possible, use an HDMI cable and connect to a tv or sound system,
the quality difference between the analog output and the HDMI is
considerable.
Wire and connect the rest of accesories as usual (wired/wireless keyboard) 

Software configuration
----------------------

Install Raspbian on the SD

https://www.raspberrypi.org/downloads/


recommend using NOOBS to install Raspbian
https://www.raspberrypi.org/downloads/noobs/


raspi-config

3 Enable Boot to Desktop/Scratch -> Desktop Log in
5 Enable Camera

Reboot

Ins

Open a console window

First, update the entire system with this two commands::
    $ sudo apt-get update
    $ sudo apt-get upgrade

Get Air Piano source code::
    $ git clone https://github.com/amcanadas/raspberry-pi-air-piano

Get into the new created folder::
    $ cd raspberry-pi-air-piano

Then, install the dependencies, starting whith OpenCV, the computer vision library::
    $ sudo apt-get install python-opencv

More complicated and time consuming is installing the resampling library, be patient. Use this commands to download/compile::
    $ wget http://www.mega-nerd.com/SRC/libsamplerate-0.1.8.tar.gz
    $ tar xvfz libsamplerate-0.1.8.tar.gz
    $ cd libsamplerate-0.1.8.tar.gz
    $ ./configure
    $ make
    $ make check

At this point, all test should be passed. Finally, install the
library and its python wrapper::
    $ sudo make install
    $ sudo ldconfig -v

    $ sudo apt-get install python-setuptools
    $ sudo apt-get install python-dev
    $ sudo easy_install scikits.samplerate

Clean samplerate sources::
    $ cd ..
    $ rm -rf libsamplerate*

Run the application
-------------------

To run the application from the command line. Type::
    $ ./play.sh

Alternativelly you can execute the application directly from
the File Manager:
1 Open File Manager (icon on the task bar).
2 Navigate to the folder where Air Piano was downloaded.
3 Double Click on play.sh. If a dialog appears, select execute.


Raspberry Pi 2 B (no overclock)
14 fps
Raspberry Pi B (no overclock)
1.8 fps
Raspberry Pi B (overclock set to High)
2.2 fps