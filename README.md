# Pacman AI implementation using Reinforcement Learning
<h2>Introduction:</h2>
The project is based on the implementation of the Pacman game and an implementation of an AI to play the game, developed using Deep Reinforcement Learning. <br>
The techniques used in this project are:
<ul><li>	Deep Learning</li>
<li>	Q Learning</li>
<li>	Simulated Annealing</li>
<li>	Heuristics</li></ul><br>
The Pacman game is implemented using pygame, and converted into a GYM environment. After that, the keras-rl library is used to make, train and test the model. 
<h2>Files:</h2>
<ul>	<li><h3>setup.py</h3>
Contains variables to set up the gym environment.  </li>
<li><h3>__init__.py</h3>
Sets up the environment. Used by gym.</li>
<li><h3>ghosts.py</h3>
Contains the class for the ghosts. Has all the functions that the ghosts need, like move, return to home, etc.</li>
<li><h3>Level.py</h3>
Contains the functions that set the level design up. Like setting all the food, superfood, walls, etc. up.</li>
<li><h3>pac.py</h3>
Contains the functions for the pacman entity. Has all the functions like move, eat, respawn, etc. (not named as such, but perform the following).</li>
<li><h3>PygamePacman.py</h3>
This is the main file with the class that gym uses to interface with the game environment. This file consists of the game loop, defined as per as the gym definition requires it. Has graphic rendering functions, game system functioning, score handling, etc.</li>
<li><h3>Screens.py</h3>
This file consists of the game over screen. Uses pygame to render the graphics.</li>
<li><h3>Pac.ipynb</h3>
This file consists of the model training script and the model testing scripts. It generates the model and tests it.</li>
<li><h3>dqn_pac-v0_weights.hp5</h3>
This is the model that is saved. Using keras-rl library.</li>
<li><h3>dqn_pac-v0_log.json</h3>
This is just a log file that keeps track of the callbacks.</li>
</ul><br>
<h2>Dependencies:</h2>
<ul><li>Python 3</li>
<li>	Pygame</li>
<li>	Keras-rl</li>
<li>	Numpy</li>
<li>	Gym</li>
<li>	Tensorflow</li>
<li>	Pip</li>
<li>	Jupyter Notebook</li></ul>
<br>
<h2>Setting up the GYM environment:</h2>
Go to the pac folder. Open command prompt/terminal from that folder. Enter:<br>
	<code>pip install -e</code><br>
This will install the environment.<br>
<h2>Execution:</h2>
Open Pac.ipynb and set the variable from:<br>
	 <code>mode = “train”</code><br>
to<br>
	<code>mode = “test”</code><br>
And run all the cells.<br>
(<u><b>NOTE</b></u>: If you wish to train the model yourself, then leave the variable as it is, and just run all the cells. Make sure the “mode” variable is set to “train” and not “test”.)<br>
<h2>Output:</h2>
A very fast game, is played. Will have to minimize the jupyter notebook, that is running the script.<br>
<img src="https://raw.githubusercontent.com/Msaif2299/Pacman/blob/master/OP.PNG"><br>
<h2>Remarks:</h2>
The AI will perform better with more training. An approximate of 20 days worth of training with better tuned parameters should get us somewhere. This model attached, is with only approximately 1 hour of training.
