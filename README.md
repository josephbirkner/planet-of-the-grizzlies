=============================================
P L A N E T   O F   T H E   G R I Z Z L I E S
=============================================

                   B E T A

-------------- 1. Dependencies --------------

- Install PyQt5 (>= Version 5.4)

  sudo apt-get install python3-pyqt5

- Install qdarkstyle

  pip3 install qdarkstyle

  Upon execution, two error messages will be
  displayed that "PyQt4" has not been found.
  Just change those imports from to "PyQt4"
  to "PyQt5", and you're good to go!


-------------- 2. How to play --------------

- cd planet_of_the_grizzlies/potg
  python3 potg.py

- Move with W A S D
- Jump witth Space
- Punch with Key Up
- Kick with Key Down


------- 3. How to become invincible --------

- Open planet_of_the_grizzlies/potg/world/potg_player.py
- Change player.max_health to 66666666