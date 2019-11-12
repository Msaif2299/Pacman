# Pacman AI implementation using Reinforcement Learning
##Introduction:
The project is based on the implementation of the Pacman game and an implementation of an AI to play the game, developed using Deep Reinforcement Learning. 
The techniques used in this project are:
•	Deep Learning
•	Q Learning
•	Simulated Annealing
•	Heuristics
The Pacman game is implemented using pygame, and converted into a GYM environment. After that, the keras-rl library is used to make, train and test the model. 
##Files:
•	###setup.py
Contains variables to set up the gym environment.  
•	###__init__.py
Sets up the environment. Used by gym.
•	###ghosts.py
Contains the class for the ghosts. Has all the functions that the ghosts need, like move, return to home, etc.
•	###Level.py
Contains the functions that set the level design up. Like setting all the food, superfood, walls, etc. up.
•	###pac.py
Contains the functions for the pacman entity. Has all the functions like move, eat, respawn, etc. (not named as such, but perform the following).
•	###PygamePacman.py
This is the main file with the class that gym uses to interface with the game environment. This file consists of the game loop, defined as per as the gym definition requires it. Has graphic rendering functions, game system functioning, score handling, etc.
•	###Screens.py
This file consists of the game over screen. Uses pygame to render the graphics.
•	###Pac.ipynb
This file consists of the model training script and the model testing scripts. It generates the model and tests it.
•	###dqn_pac-v0_weights.hp5
This is the model that is saved. Using keras-rl library.
•	###dqn_pac-v0_log.json
This is just a log file that keeps track of the callbacks.
###Dependencies:
•	Python 3
•	Pygame
•	Keras-rl
•	Numpy
•	Gym
•	Tensorflow
•	Pip
•	Jupyter Notebook
###Setting up the GYM environment:
Go to the pac folder. Open command prompt/terminal from that folder. Enter:
	```pip install -e```
This will install the environment.
###Execution:
Open Pac.ipynb and set the variable from:
	```mode = “train”```
to
	```mode = “test”```
And run all the cells.
(NOTE: if you wish to train the model yourself, then leave the variable as it is, and just run all the cells. Make sure the “mode” variable is set to “train” and not “test”.
##Output:
A very fast game, is played. Will have to minimize the jupyter notebook, that is running the script.
##Remarks:
The AI will perform better with more training. An approximate of 20 days worth of training with better tuned parameters should get us somewhere. This model attached, is with only approximately 1 hour of training.
