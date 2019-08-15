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
        if board[self.x][self.y] in [2, 3, 5, 0]:
            board[self.x][self.y] = 7
        return self.__direction()

class blinky:
    def __init__(self):
        self.x = 12
        self.y = 14
        self.direction = 'right'

    def neighbors(self):
        pass

    def move(self, pac, board):
        if board[pac.x + pac.vx][pac.y + pac.vy] != 1:
            pass


if __name__ == '__main__':
    from Level import level
    from os import system
    from msvcrt import getch, kbhit
    g = level()
    g.setWalls()
    g.setFood()
    p = pacman()
    direction = 'down'
    count = 0
    while True:
        if kbhit():
            key = ord(getch())
            if key == 72:
                    direction = 'left'
            elif key == 75:
                    direction = 'up'
            elif key == 80:
                    direction = 'right'
            elif key == 77:
                    direction = 'down'
            print(direction)
        g.printBoardasBlx()
        if count == 10:
            p.move(direction, g.board)
            count = 0
        system("cls")
        count += 1
