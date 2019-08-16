class pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.vx = 0
        self.vy = 1

    def __direction(self):
        if self.vx == 1 and self.vy == 0:
            return 'down'
        if self.vx == -1 and self.vy == 0:
            return 'up'
        if self.vx == 0 and self.vy == 1:
            return 'right'
        if self.vx == 0 and self.vy == -1:
            return 'left'
        raise Exception('Unknown direction')

    def move(self, d, board):
        if self.y + self.vy == 28:
            board[self.x][self.y] = 0
            self.y = 0
            board[self.x][self.y] = 7
            return  self.__direction()
        if self.y + self.vy == -1:
            board[self.x][self.y] = 0
            self.y = 27
            board[self.x][self.y] = 7
            return  self.__direction()
        if d == 'up':
            if board[self.x-1][self.y] != 1:
                self.vx = -1
                self.vy = 0
        elif d == 'down':
            if board[self.x+1][self.y] != 1:
                self.vx = 1
                self.vy = 0
        elif d == 'left':
            if board[self.x][self.y-1] != 1:
                self.vx = 0
                self.vy = -1
        elif d == 'right':
            if board[self.x][self.y+1] != 1:
                self.vx = 0
                self.vy = 1
        if board[self.x+self.vx][self.y+self.vy] == 1:
            return  self.__direction()
        board[self.x][self.y] = 0
        self.x += self.vx
        self.y += self.vy
        if board[self.x][self.y] in [2, 3, 5, 0, 6]:
            board[self.x][self.y] = 7
        return self.__direction()

class blinky:
    def __init__(self):
        self.x = 11
        self.y = 14
        self.direction = 'right'
        self.prev = 0

    def neighbors(self, board):
        possibilities = [(self.x-1, self.y, 'up'), (self.x, self.y-1, 'left'), (self.x+1, self.y, 'down'), (self.x, self.y+1, 'right')]
        if self.direction == 'down':
            possibilities.remove((self.x-1, self.y, 'up'))
        elif self.direction == 'up':
            possibilities.remove((self.x+1, self.y, 'down'))
        elif self.direction == 'right':
            possibilities.remove((self.x, self.y-1, 'left'))
        elif self.direction == 'left':
            possibilities.remove((self.x, self.y+1, 'right'))
        else:
            raise Exception('Unknown Direction')
        for x, y, z in possibilities:
            if (x == 14 and y == 5) or (y == 22 and x == 14) or board[x][y] == 1:
                continue
            else:
                yield (x, y, z)

    def move(self, pac, board):
        pactomove = [pac.x + 2*pac.vx, pac.y + 2*pac.vy]
        dist = 20000
        nextmove = [0, 0, None]
        for x, y, z in self.neighbors(board):
            temp = (pactomove[0] - x)**2 + (pactomove[1] - y)**2
            if temp < dist:
                dist = temp
                nextmove = [x, y, z]
        board[self.x][self.y] = self.prev
        if board[self.x][self.y] == 7:
            board[self.x][self.y] = 0
        self.prev = board[nextmove[0]][nextmove[1]]
        board[nextmove[0]][nextmove[1]] = 4
        self.direction = nextmove[2]
        self.x = nextmove[0]
        self.y = nextmove[1]
        return self.direction


