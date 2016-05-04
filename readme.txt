README

To run on a computer in Fitzpatrick:
git clone https://github.com/rmcgrai1/PyGame-Project.git
python client.py

GAMEPLAY:
Connect to the sever, and try to shoot down anyone else online!
Don't get yourself shot, though.
And do lots of barrel rolls! (press b)

CONTROLS:
w is boost forwards, s is brakes
a and d spin the view
r is respawn
b is BARREL ROLL
click to fire
Mouse to move around the screen
Don't run into the asteroids, you will take damage!


To run, you must:
- have pip
- have a C++ compiler linked with python
- set up distutils.cfg
- run "python setup.py install" to install the canv3d module
- run "pip install pygame" to install the pygame library
- run "pip install numpy" to install the numpy array library
- run "pip install twisted" to install the twisted networking library


Known Bugs:
- lasers occasionally appear behind player (due to latency over connection)
- seg-faults occasionally occur as game is closed (uncertain cause)