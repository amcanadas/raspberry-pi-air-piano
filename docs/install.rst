.. _install:

Installing and configuring Air Piano
====================================

Hardware Requirements
---------------------
* Raspberry Pi Model B or Raspberry Pi 2 Model B.
* SD Card (you can check recomend SD card size an type at https://www.raspberrypi.org/documentation/installation/sd-cards.md).
* Camera Module (https://www.raspberrypi.org/products/camera-module/)
* HDMI cable and USB charger
* Optional: wireless keyboard/mouse


Hardware configuration
----------------------

Install the camera module, check https://www.raspberrypi.org/help/camera-module-setup/ if
you have not done it before.

When possible, use an HDMI cable and connect to a tv or sound system,
the quality difference between the analog output and HDMI is
considerable.

Wire and connect the rest of accesories as usual (wired/wireless keyboard, wifi, etc.). This
configurations are not included here, as they are aside of this project.


Software configuration
----------------------

Install Raspbian on the SD. The download page is at https://www.raspberrypi.org/downloads/

I personally recommend using NOOBS to install Raspbian (https://www.raspberrypi.org/downloads/noobs/)

Follow the instructions given in the download page.

In order to use Air Piano, the camera module must be enabled and the Pi should boot to graphical
desktop. This can be configured with raspi-config utility. Open a terminal and type::

    $ sudo raspi-config

Select this two options and activate the desired options:

* 3 Enable Boot to Desktop/Scratch -> Desktop Log in
* 5 Enable Camera -> Enable

Reboot the Pi

Installing the application and its requirements
-----------------------------------------------

1. Open a terminal window.

2. First, update the entire system with this two commands::

    $ sudo apt-get update
    $ sudo apt-get upgrade

3. Get Air Piano source code::

    $ git clone https://github.com/amcanadas/raspberry-pi-air-piano

4. Get into the new created folder::

    $ cd raspberry-pi-air-piano

5. Then, install the dependencies, starting whith OpenCV, the computer vision library::

    $ sudo apt-get install python-opencv

6. More complicated and time consuming is installing the resampling library, be patient. Use this commands to download/compile::

    $ wget http://www.mega-nerd.com/SRC/libsamplerate-0.1.8.tar.gz
    $ tar xvfz libsamplerate-0.1.8.tar.gz
    $ cd libsamplerate-0.1.8.tar.gz
    $ ./configure
    $ make
    $ make check

7. At this point, all test should be passed. Finally, actually install the
library and its python wrapper::

    $ sudo make install
    $ sudo ldconfig -v
    $ sudo apt-get install python-setuptools
    $ sudo apt-get install python-dev
    $ sudo easy_install scikits.samplerate

8. All requirements installed!. Cleanup::

    $ cd ..
    $ rm -rf libsamplerate

Run the application
-------------------

Option 1: from command line.
............................

To run the application from the command line. Type::

    $ ./play.sh

Option 2: graphical
...................

Alternativelly you can execute the application directly from
the File Manager:

1. Open File Manager (icon on the task bar).
2. Navigate to the folder where Air Piano was downloaded.
3. Double Click on play.sh. If a dialog appears, select *Execute*.