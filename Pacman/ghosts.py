from random import randint
class ghosts:
    '''
    Class representing the 4 ghosts :
        1. Blinky -> Red Ghost (Follows very closely, homes on Pacman's location)
        2. Pinky -> Pink Ghost (Tries to land 4 steps ahead of Pacman)
        3. Inky -> Cyan Ghost (Mood swings, sometimes tries to land 4 steps ahead, sometimes runs away)
        4. Clyde -> Brown Ghost (If far away, homes in on Pacman, if too close, tries to run away, if between, makes random moves)
    '''
    def __init__(self):
        '''
        Setting Blinky (Red Ghost) only free. Trapping the rest of the ghosts in the box in the middle of the level.
        '''
        self.ghosts = {}
        self.GHOSTS = ["Inky", "Pinky", "Clyde", "Blinky"]
        for g in self.GHOSTS:
            self.ghosts[g] = {}
            for var, val in zip(["x", "y", "direction", "trapped", "frightened", "eaten", "trappedTime"], [14, 11, 'right', True, False, False, 0]):
                self.ghosts[g][var] = val
        self.ghosts["Blinky"]['x'] = 11    #Coordinates of Blinky (x, y) -> (blinkx, blinky)
        self.ghosts["Blinky"]['y'] = 14    
        self.ghosts["Blinky"]['direction'] = 'right'   #Direction of Blinky, facing 'right'
        self.ghosts["Inky"]['x'], self.ghosts["Inky"]['y'], self.ghosts["Inky"]['direction'], self.ghosts["Inky"]['trapped'] = 14, 11, 'right', True
        #Setting coordinates and direction of Inky (x, y, direction) -> (inkx, inky, inkdirection)
        self.ghosts["Pinky"]['x'], self.ghosts["Pinky"]['y'], self.ghosts["Pinky"]['direction'], self.ghosts["Pinky"]['trapped'] = 14, 16, 'left', True
        #Setting coordinates and direction of Pinky (x, y, direction) -> (pinkx, pinky, pinkdirection)
        self.ghosts["Clyde"]['x'], self.ghosts["Clyde"]['y'], self.ghosts["Clyde"]['direction'], self.ghosts["Clyde"]['trapped'] = 14, 11, 'right', True
        #Setting coordinates and direction of Clyde (x, y, direction) -> (clydex, clydey, clydedirection)
        self.ghosts["Blinky"]['trapped'] = False
        for g, time in zip(["Blinky", "Inky", "Pinky", "Clyde"], [i*50 for i in range(4)]):
            self.ghosts[g]['trappedTime'] = time
        

    def neighbors(self, board, currx, curry, currdir):
        '''
        Find the possible boxes which the ghost can go into (only in the 4 CARDINAL DIRECTIONS)
        Rules:
            1. Will not enter a box with value 1 (as it is a wall).
            2. If facing a direction, will not suddenly go in the opposite direction.
            3. If faced with multiple options, priority is as follows:
                a. up
                b. left
                c. down
                d. right
            4. Will not enter into the hallway which teleports Pacman (hard-coded coordinates).

        Args:
            board   -> 2D matrix representing the Pacman board (2D int matrix)
            currx   -> Current x coordinate (x -> rows)
            curry   -> Current y coordinate (y -> columns)
            currdir -> Current direction (string)

        Yields:
            All the possible moves.
            (x, y, direction) -> Coordinates and Direction of the possible move
        '''
        possibilities = [(currx-1, curry, 'up'), (currx, curry-1, 'left'), (currx+1, curry, 'down'), (currx, curry+1, 'right')]
        #possible moves with the coordinates and directions in the form of an array and in the priority order
        if currdir == 'down':   #if current direction is down, then remove 'up' so that ghost does not flip directions
            possibilities.remove((currx-1, curry, 'up'))    #remove 'up'
        elif currdir == 'up':   #if current direction is up, then remove 'down' so that ghost does not flip directions
            possibilities.remove((currx+1, curry, 'down'))  #remove 'down'
        elif currdir == 'right':#if current direction is right, then remove 'left' so that ghost does not flip directions
            possibilities.remove((currx, curry-1, 'left'))  #remove 'left'
        elif currdir == 'left': #if current direction is left, then remove 'right' so that ghost does not flip directions
            possibilities.remove((currx, curry+1, 'right')) #remove 'right'
        else:   #unknown direction has been detected
            raise Exception('Unknown Direction')    #raise Exception
        for x, y, z in possibilities:   #iterate through every possible move
            if (x == 14 and y == 5) or (y == 22 and x == 14) or board[x][y] == 1:   #if the move is a part of the hallway, or is a wall
                continue    #then just don't yield it
            else:   #means a valid move has been found
                yield (x, y, z) #then yield it

    def pursuemove(self, pactomove, board, nextx, nexty, nextdir):
        '''
        Function that tells which move to follow, if pursuing Pacman.
        Choose the tile that is closest to Pacman, using the Distance Formula between two points.
            d = (x1 - x0)^2 + (y1 - y2)^2

        Args:
            pactomove   -> Array with the coordinates to pursue  (int array of size 2 representing [x, y])
            board       -> 2D matrix of Pacman game (2D int matrix)
            nextx       -> Ghost's x coordinate (x -> row)
            nexty       -> Ghost's y coordinate (y -> column)
            nextdir     -> Ghost's current direction (string)

        Returns:
            nextmove    -> Array of [x, y, direction] of the next move
        '''
        dist = 20000    #minimum distance to Pacman
        nextmove = [0, 0, None]     #setting the nextmove to empty values
        for x, y, z in self.neighbors(board, nextx, nexty, nextdir):    #iterating over every possible move
            temp = (pactomove[0] - x)**2 + (pactomove[1] - y)**2    #calculate the distance
            if temp < dist:     #if a smaller distance has been found (notice how it only considers the lower value and not the equal value)
                #this is done to preserve the priority order of moves (up, left, down, right)
                dist = temp     #keep track of the minimum distance found
                nextmove = [x, y, z]    #keep track of the move for the minimum distance
        return nextmove     #return the minimum distance move

    def clydemove(self, pactomove, board, nextx, nexty, nextdir):
        '''
        Function to move like Clyde (Brown Ghost).
        Distance is calculated using the Distance Formula between two points:
            d = (x1 - x0)^2 + (y1 - y2)^2
        Rules:
            If distance between (nextx, nexty) and pactomove:
                1. greater than 100:
                    Then pursue Pacman
                2. greater than 81 but less than or equal to 100:
                    Then move randomly
                3. less than or equal to 81:
                    Then move to the tile furthest from Pacman from the possible moves
        Args:
            pactomove   -> Array representing location to move to (pacman's location) and is of type [x, y]
            board       -> 2D matrix representing the Pacman game (2D int matrix)
            nextx       -> Ghost's x coordinates (x -> row)
            nexty       -> Ghost's y coordinates (y -> column)
            nextdir     -> Ghost's current direction
        Returns:
            nextmove    -> [x, y, direction] : array representing the next move the ghost will take
        '''
        dist = -20000   #distance to maximize
        temp = (pactomove[0] - nextx)**2 + (pactomove[1] - nexty)**2    #calculate the distance between Pacman and the Ghost
        if temp > 100:  #if distance is greater than 100
            return self.pursuemove(pactomove, board, nextx, nexty, nextdir) #then pursue Pacman
        if temp > 81 and temp <= 100:   #if distance lies between 81 and 100, move randomly
            maxr = 0    #find the move which generated the maximum random value
            for x, y, z in self.neighbors(board, nextx, nexty, nextdir):    #in all possible moves
                r = randint(1, 100) #generate the random number
                if maxr < r:    #if the generated random number is greater than the current max
                    nextmove = [x, y, z]    #store the move
                    maxr = r                #store the max number
            return nextmove     #return the move which had the max random number generated
        for x, y, z in self.neighbors(board, nextx, nexty, nextdir):    #if the distance is less than 81
            temp = (pactomove[0] - x)**2 + (pactomove[1] - y)**2    #calculate the distance
            if temp > dist:             #if the distance is greater than the current max distance
                dist = temp             #then store this distance
                nextmove = [x, y, z]    #and store the move
        return nextmove                 #now return the furthest move from Pacman

    def inkmove(self, pac, board, nextx, nexty, nextdir):
        '''
        Function to move like Inky (Blue Ghost). Mood swings.
        Rules:
            50 - 50 chance to do either of the following:
                1. Move like Pinky (Pink Ghost) (Move 4 spaces ahead of Pacman).
                2. Move like Clyde (Brown Ghost) (Move away or randomly or towards Pacman)
        Args:
            pac     -> Pacman object (Needed for the coordinates)
            board   -> 2D matrix representing the Pacman game (2D int matrix)
            nextx   -> Ghost's x coordinates (x -> row)
            nexty   -> Ghost's y coordinates (y -> column)
            nextdir -> Ghost's current direction

        Returns:
            A list consisting of [x, y, direction]
                where, x         -> next move's x coordinate
                       y         -> next move's y coordinate
                       direction -> next move's direction
        '''
        r = randint(1, 100) #generate a random number between 1, 100
        if r <= 50: #if number is lesser than 50, move like Inky
            return self.pursuemove([pac.x + 4*pac.vx, pac.y + 4*pac.vy], board, nextx, nexty, nextdir)
        return self.clydemove([pac.x, pac.y], board, nextx, nexty, nextdir)
        #if number is greater is than 50, move like Clyde

    def trappedmove(self, nextx, nexty, nextdir):
        '''
        Function to generate sideway movements when inside the box.
        Args:
            nextx   -> Ghost's x coordinates (x -> row)
            nexty   -> Ghost's y coordinates (y -> column)
            nextdir -> Ghost's current direction
        Returns:
            A list consisting of [x, y, direction]
                where, x         -> next move's x coordinate
                       y         -> next move's y coordinate
                       direction -> next move's direction
        '''
        if nextx == 14 and nexty == 11:     #if the ghost is travelling towards the left end of the box
            if nextdir == 'left':   #check if it is crashing into the wall
                return [nextx, nexty+1, 'right']    #then flip the direction and return the new coordinates
        if nextx == 14 and nexty == 16:     #if the ghost is travelling towards the right end of the box
            if nextdir == 'right':  #check if it is crashing into the wall
                return [nextx, nexty-1, 'left']     #then flip the direction and return the new coordinates
        if nextdir == 'left':   #check if the ghost is travelling towards left
            return [nextx, nexty-1, 'left']     #if so, then reduce the column number by one and return the new coordinates
        return [nextx, nexty+1, 'right']    #this means the ghost is travelling towards right, then increase the column number by one, and then return the new coordinates

    def setFree(self, string):
        '''
        Function to free the ghosts from their box.
        Args:
            string  -> name of the ghost 
        Returns:
            Nothing
        '''
        if string == 'Inky':    #if the ghost is Inky
            self.ghosts["Inky"]['x'], self.ghosts["Inky"]['y'], self.ghosts["Inky"]['direction'] = 11, 14, 'left'        #then set its coordinates to outside the box
        elif string == 'Pinky': #if the ghost is Pinky
            self.ghosts["Pinky"]['x'], self.ghosts["Pinky"]['y'], self.ghosts["Pinky"]['direction'] = 11, 14, 'right'    #then set its coordinates to outside the box
        elif string == 'Clyde': #if the ghost is Clyde
            self.ghosts["Clyde"]['x'], self.ghosts["Clyde"]['y'], self.ghosts["Clyde"]['direction'] = 11, 14, 'right'  #then set its coordinates to outside the box
        elif string == 'Blinky':    #if the ghost is Blinky
            self.ghosts["Blinky"]['x'], self.ghosts["Blinky"]['y'], self.ghosts["Blinky"]['direction'] = 11, 14, 'right' #then set its coordinates to outside the box

    def frightenedmove(self, board, pac, nextx, nexty, nextdir):
        '''
        Function to move randomly when frightened
        Args:
            board       -> 2D int matrix for pacman game
            pac         -> pacman object
            nextx       -> x coordinate of the ghost
            nexty       -> y coordinate of the ghost
            nextdir     -> direction the ghost is currently facing (string)
        Returns:
            nextmove    -> List consisting of x, y coordinates and directions for the next move
        '''
        dist = -2000
        nextmove = [0, 0, None]
        for x, y, z in self.neighbors(board, nextx, nexty, nextdir):
            temp = (pac.x - x)**2 + (pac.y - y)**2
            if temp > dist:
                dist = temp
                nextmove = [x, y, z]
        return nextmove

    def movebacktohouse(self, board, nextx, nexty, nextdir, trapped, eaten):
        '''
        Function to move back to the ghost house once they have been eaten
        Args:
            board       -> 2D int matrix for pacman game
            nextx       -> x coordinate of the ghost
            nexty       -> y coordinate of the ghost
            nextdir     -> direction the ghost is currently facing (string)
            trapped     -> boolean that represents if the ghost is trapped or not
            eaten       -> boolean that represents if the ghost is eaten or not
        Returns:
            nextmove    -> a list of values that have to be returned consisting of:
                            1. x coordinate
                            2. y coordinate
                            3. direction
                            4. trapped
                            5. eaten
        '''
        if (nextx == 11 and nexty == 14) or (nextx == 11 and nexty == 13):  #if the coordinates are either (11, 14) or (11, 13)
            return [14, 11, 'right', True, False, 50]   #trap them
        t = self.movetoposition(board, [11, 14], nextx, nexty, nextdir)
        t.extend([False, True, 0])
        return t
        #return the values to be assigned


    def movetoposition(self, board, position, nextx, nexty, nextdir):
        '''
        Function to aim for a position and have the ghosts move to it
        Args:
            board       -> 2D int matrix for pacman game
            position    -> x and y coordinates of the position to aim for
            nextx       -> x coordinate of the ghost
            nexty       -> y coordinate of the ghost
            nextdir     -> direction the ghost is currently facing (string)
        Returns:
            nextmove    -> List consisting of x, y coordinates and directions for the next move
        '''
        dist = 20000    #set the distance to a default to calculate the min distance from the available moves
        nextmove = [0, 0, None] #the next move, set to default
        for x, y, z in self.neighbors(board, nextx, nexty, nextdir):    #for every possible move
            temp = (x - position[0])**2 + (y - position[1])**2  #calculate the distance
            if temp < dist: #if it is lesser than previous min distance
                dist = temp #set it as the min distance
                nextmove = [x, y, z]    #and record the move needed to achieve it
        return nextmove #return the minimum distance move

    def eatenHandler(self, pac):
        x, y = pac.x, pac.y
        oldx, oldy = pac.oldx, pac.oldy
        direction = pac.direction()
        t = 0
        for g in self.GHOSTS:
            if not self.ghosts[g]['eaten'] and self.ghosts[g]['frightened']:
                if self.ghosts[g]['x'] == x:
                    if self.ghosts[g]['y'] == y or (self.ghosts[g]['y'] == oldy and direction != self.ghosts[g]['direction']):
                        self.ghosts[g]['eaten'] = True
                        t += 1
                elif self.ghosts[g]['y'] == y:
                    if self.ghosts[g]['x'] == x or (self.ghosts[g]['x'] == oldx and direction != self.ghosts[g]['direction']):
                        self.ghosts[g]['eaten'] = True
                        t += 1
        return t
    def move(self, pac, board, scatter=False, frighten=False):
        '''
        Function to move the ghosts.
        Args:
            pac     -> The Pacman object (For coordinates)
            board   -> 2D matrix for the Pacman game
            scatter -> boolean that tells the ghost to scatter or not
        Returns:
            Nothing
        '''
        #Blinky is generally free. So we just use Pursue on it.
        for g, pos in zip(self.GHOSTS, [(28, 26), (1, 1), (28, 1), (1, 26)]):
            if not self.ghosts[g]['trapped'] and not self.ghosts[g]['eaten']:
                if frighten:
                    self.ghosts[g]['frightened'] = True
                    self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'] = self.frightenedmove(board, pac, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                else:
                    self.ghosts[g]['frightened'] = False
                    if not scatter: #if scatter is not set, then pursue
                        nextmove = [0, 0, None]
                        if g == "Blinky":
                            nextmove =  self.pursuemove([pac.x, pac.y], board, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                        elif g == "Pinky":
                            nextmove = self.pursuemove([pac.x + 4*pac.vx, pac.y + 4*pac.vy], board, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                        elif g == "Inky":
                            nextmove = self.inkmove(pac, board, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                        else:
                            nextmove = self.clydemove([pac.x, pac.y], board, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                        self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'] = nextmove
                    elif scatter:   #if scatter is set, then aim for the corner piece (1, 26)
                        self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'] = self.movetoposition(board, [1, 26], self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
            else:
                if not self.ghosts[g]['eaten']:
                    self.ghosts[g]['trappedTime'] -= 1
                    if self.ghosts[g]['trappedTime'] == 0:
                        self.ghosts[g]['trapped'] = False
                        self.setFree(g)
                    else:
                        self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'] = self.trappedmove(self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'])
                else:
                    self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'], self.ghosts[g]['trapped'], self.ghosts[g]['eaten'], self.ghosts[g]['trappedTime'] = self.movebacktohouse(board, self.ghosts[g]['x'], self.ghosts[g]['y'], self.ghosts[g]['direction'], self.ghosts[g]['trapped'], self.ghosts[g]['eaten'])

       