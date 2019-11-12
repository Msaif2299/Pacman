from random import randint

class pacman:
    '''
    Class representing the Pacman object
    '''
    def __init__(self):
        '''
            x, y   -> Coordinates of the Pacman (x = rows, y = columns)
            vx, vy -> Velocities of the Pacman (vx = vertical velocity, vy = horizontal velocity)

            Default Settings:
                Starting coordinates = (1, 1)
                Starting Velocities = (0, 1)
                Starting Direction = Right
        '''
        self.oldx = 0
        self.oldy = 0
        self.x = 1
        self.y = 1
        self.vx = 0
        self.vy = 1
        self.lives = 3


    def __direction(self):
        '''
        Private Function to get direction for given velocity (vx, vy)

        Returns:
            string -> Directions according to vx, vy

        Raises:
            Unknown Direction Exception in case an undefined (vx, vy) is detected.
        '''
        if self.vx == 1 and self.vy == 0:   #return 'down' if vx is 1
            return 'down'
        if self.vx == -1 and self.vy == 0:  #return 'up' if vx is -1
            return 'up'
        if self.vx == 0 and self.vy == 1:   #return 'right' if vy is 1
            return 'right'
        if self.vx == 0 and self.vy == -1:  #return 'left' is vy is -1
            return 'left'
        raise Exception('Unknown direction')    #raise exception if not part of the FOUR CARDINAL DIRECTIONS

    def direction(self):
        return self.__direction()

    def move(self, d, board):
        '''
        Function that updates the x and y values of the Pacman and vx and vy values according to the given direction

        Args:
              d   -> direction      (string)
            board -> Pacman board   (2D int matrix)

        Returns:
            self.__direction() -> direction from values of current (vx, vy)     (type = string)
        '''
        if self.y + self.vy == 28:      #teleporting mechanic for the right most side
        #logic is that, the only time the pacman will ever reach this column when it enters this hallway
        #so, catch that case and teleport him to the other end of that hallway
            board[self.x][self.y] = 0   #setting this side of the hallway as empty
            self.y = 0                  #teleporting pacman to the other side of the hallway
            board[self.x][self.y] = 7   #setting the location of pacman on the board
            return  [self.__direction(), 0]  #returning the direction of pacman
        if self.y + self.vy == -1:      #same logic as before, the only time this happens is when it is in the hallway
            board[self.x][self.y] = 0   #setting this side of the hallway as empty
            self.y = 27                 #teleporting pacman to the other end of the hallway
            board[self.x][self.y] = 7   #setting the location fo pacman on the board
            return [self.__direction(), 0]  #returning the direction of pacman
        if d == 'up':                   #if the direction to change is 'up'
            if (self.x-1 >= 0) and board[self.x-1][self.y] != 1:    #checking if there is nothing blocking it
                self.vx = -1            #changing the vertical velocity
                self.vy = 0             #changing the horizontal velocity
        elif d == 'down':               #checking if the direction to change is 'down'
            if (self.x + 1 < len(board)) and board[self.x+1][self.y] != 1:    #checking if nothing is blocking it
                self.vx = 1             #changing the vertical velocity
                self.vy = 0             #changing the horizontal velocity
        elif d == 'left':               #checking if the direction to change is 'left'
            if (self.y - 1 >= 0) and board[self.x][self.y-1] != 1:    #checking if nothing is blocking it
                self.vx = 0             #changing the vertical velocity
                self.vy = -1            #changing the horizontal velocity
        elif d == 'right':              #checking if the direction to change is 'right'
            if (self.y + 1 < len(board[0])) and board[self.x][self.y+1] != 1:    #checking if nothing is blocking it
                self.vx = 0             #changing the vertical velocity
                self.vy = 1             #changing the horizontal velocity
        if self.x + self.vx < len(board) and self.vy + self.y < len(board[0]) and board[self.x+self.vx][self.y+self.vy] == 1:  #if the direction is blocked, then just return the direction
            return  [self.__direction(), 0]  #returning the direction
        if self.x + self.vx >= len(board) or self.y + self.vy >= len(board[0]):
            return [self.__direction(), 0]
        board[self.x][self.y] = 0       #set the location on the board to 0, because if there was anything, it got eaten
        self.oldx = self.x
        self.oldy = self.y
        self.x += self.vx               #update the x coordinate by adding the vertical velocity (x -> row)
        self.y += self.vy               #update the y coordinate by adding the horizontal velocity (y -> column)
        if board[self.x][self.y] in [2, 3, 5, 0]:    #if the new values are anything like normal pellets, or empty, or super pellets, just set them to 0, as they have now been eaten
            t = board[self.x][self.y]
            board[self.x][self.y] = 7   #setting the location to hold the new coordinates of the pacman
            return [self.__direction(), t]       #return the direction of the pacman
        board[self.x][self.y] = 7
        return [self.__direction(), 6] 

