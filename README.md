PLANET OF THE GRIZZLIES
=======================

B E T A

1.1 Dependencies
---------------

- Install PyQt5 (>= Version 5.4)

    \# Only works in Ubuntu/Debian >= 14.04
    sudo apt-get install python3-pyqt5

- Install qdarkstyle

    pip3 install qdarkstyle

*Upon execution, two error messages will be displayed that "PyQt4" has not been found. Just change those imports from `PyQt4` to `PyQt5`, and you're good to go!*

1.2 Installing PyQt5 with EGL support on Raspbian Jessy to enable hardware acceleration
---------------------------------------------------------------------------------------

- Link GPU eglfs binaries so Qt can get to them in system path

    sudo mv /usr/lib/arm-linux-gnueabihf/libEGL.so.1.0.0.bak
    sudo mv /usr/lib/arm-linux-gnueabihf/libGLESv2.so.2.0.0.bak
    sudo ln -s /opt/vc/lib/libEGL.so /usr/lib/arm-linux-gnueabihf/libEGL.so.1.0.0
    sudo ln -s /opt/vc/lib/libGLESv2.so /usr/lib/arm-linux-gnueabihf/libGLESv2.so.2.0.0

- Install the leandog apt server in your sources

    echo "deb http://apt.leandog.com/ jessie main" | sudo tee --append /etc/apt/sources.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BDCBFB15

- Install packages

    sudo apt-get update
    sudo apt-get install -y qt5 sip pyqt5

- Install qdarkstyle

    sudo pip3 install qdarkstyle

- Increase the Raspberrie's video memory

    sudo raspi-config
    > *Memory Split*
    > Enter 256
    > Confirm, Exit, Reboot

- It might be necessary to tune down the ingame graphics

    To do so, first open planet_of_the_grizzlies/potg/network/potg_client.py
    Change `Client.gfxmode` from `0` to `World.DisableBackgrounds`

2. How to play
--------------

    cd planet_of_the_grizzlies/potg
    python3 potg.py

- Move with W A S D
- Jump with Space
- Punch with Key Up
- Kick with Key Down


3. How to become invincible
---------------------------

- Open planet_of_the_grizzlies/potg/world/potg_player.py
- Change `Player.max_health` to 66666666