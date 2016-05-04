README

To run on a Linux computer in Fitzpatrick:
Navigate to the directory where you will be running this game. Type:
git clone https://github.com/rmcgrai1/PyGame-Project.git
(Alternatively, unzip the file we e-mailed)

Now open another terminal. On that terminal:
ssh student00.cse.nd.edu

On student00, cd to the running directory. Once there, type:
python server.py

On the first terminal on the local fitz machine: 
python client.py

The game has now started!


If you have any problems, type:
python setup.py build
cp buid/lib.linux-YOUR_COMPUTER_SPECS/canv3d.so ./

Your computer specs should be the last thing printed out after running python setup.py build. We pre-built for build/lib.linux-x86_64-2.6, but some machines in the library are 2.7


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
