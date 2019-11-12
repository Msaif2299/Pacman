import gym
import os
from gym import error, spaces, utils
from gym.utils import seeding
import pygame
from .pacman import pacman
from .ghosts import ghosts
from .Level import level
from .Screens import winScreen
from .PygamePacman import *

class PacmanPygame(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.actions = {}
        a = 0
        for f_direction in ['left', 'right', 'up', 'down']:
            for s_direction in ['left', 'right', 'up', 'down']:
                self.actions[a] = [f_direction, s_direction]
                a += 1
        self.game = level()
        self.game.setWalls()
        self.game.setWalls()
        self.game.setFood()
        self.p = pacman()
        pygame.init()
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)
        self.boxSize = 25
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        #print(self.__dict__)
        self.text = self.font.render('Score: 0', True, self.YELLOW, self.BLACK)
        self.scoreSprite = {}
        dir_name = os.path.dirname(__file__)
        for score in [(2**i)*100 for i in range(1, 5)]:
            self.scoreSprite[score] = pygame.transform.scale(pygame.image.load(os.path.join(dir_name,'./images/{}.png'.format(score))), (self.boxSize, self.boxSize))
        self.scoreRect = self.text.get_rect()
        self.width = 28
        self.height = 30
        self.score = 0
        self.ghosts_combo = 0
        self.gameDisplay = None
        self.scoreRect.center = (self.width*self.boxSize + 100, 50)
        pygame.display.set_caption("Pacman")
        self.grid = []
        self.food_sprite = pygame.image.load(os.path.join(dir_name,"./images/Food.png"))
        self.food_sprite = pygame.transform.scale(self.food_sprite, (self.boxSize, self.boxSize))
        self.superfood_sprite = pygame.transform.scale(pygame.image.load(os.path.join(dir_name,"./images/SuperFood.png")), (self.boxSize, self.boxSize))
        self.pac_sprite = [None]*3
        self.ghost_sprite = {}
        GHOST_NAMES = ["Blinky", "Pinky", "Inky", "Clyde", "EatenGhost"]
        CARDINAL_DIRECTIONS = ["Up", "Down", "Left", "Right"]
        for gh in GHOST_NAMES:
            self.ghost_sprite[gh] = {}
        for gh in self.ghost_sprite.keys():
            for direction in CARDINAL_DIRECTIONS:
                self.ghost_sprite[gh][direction.lower()] = pygame.transform.scale(pygame.image.load(os.path.join(dir_name,"./images/" + gh + direction + ".png")), (self.boxSize, self.boxSize))
        for i in range(1,4):
            self.pac_sprite[i-1] = pygame.image.load(os.path.join(dir_name,"./images/Pac" + str(i) + ".png"))
            self.pac_sprite[i-1] = pygame.transform.scale(self.pac_sprite[i-1], (self.boxSize, self.boxSize))
        self.frightened_ghost = pygame.transform.scale(pygame.image.load(os.path.join(dir_name,"./images/Scared.png")), (self.boxSize, self.boxSize))
        self.ghost = ghosts()
        self.count = 0
        self.pellets = sum([row.count(2) for row in self.game.board])
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                temp.append(pygame.Rect(j*self.boxSize, i*self.boxSize, self.boxSize, self.boxSize))
            self.grid.append(temp)
        self.pac = getNextSprite('right', self.count, self.pac_sprite)
        self.bsprite = self.ghost_sprite["Blinky"][self.ghost.ghosts["Blinky"]['direction']]
        self.pinksprite = self.ghost_sprite["Pinky"][self.ghost.ghosts["Pinky"]['direction']]
        self.clydesprite = self.ghost_sprite["Clyde"][self.ghost.ghosts["Clyde"]['direction']]
        self.inksprite = self.ghost_sprite["Inky"][self.ghost.ghosts["Inky"]['direction']]
        self.tick = 0  
        self.slower = 1
        self.scatter = True
        self.phase = 1
        self.level = 1
        self.scatterLevel = {1: [[14, 40], [14, 40], [10, 40], [10, 'inf']], 
                        2: [[14, 40], [14, 40], [10, 1033], [10, 'inf']]}
        self.frightenTimer = {1: 40, 2: 20}
        self.frightenTimeLeft = 0
        self.sprite_show_time = 0
        self.sprite_x, self.sprite_y = 0, 0
        self.sprite_value = 0
        self.scatterTime = self.scatterLevel[self.level][self.phase-1][0]
        self.chaseTime = self.scatterLevel[self.level][self.phase-1][1]
        self.gameOver = False
        self.slower = 0
        self.reward = 0

    def __featureGenerator(self):
        directions = {'left': 0, 'right': 1, 'down': 2, 'up': 3}
        features = [self.p.x, self.p.y, self.p.oldx, self.p.oldy]
        for ghost in self.ghost.GHOSTS:
            features.append(self.ghost.ghosts[ghost]['x'])
            features.append(self.ghost.ghosts[ghost]['y'])
            features.append(directions[self.ghost.ghosts[ghost]["direction"]])
            features.append(self.ghost.ghosts[ghost]["trapped"])
            features.append(self.ghost.ghosts[ghost]["frightened"])
            features.append(self.ghost.ghosts[ghost]["eaten"])
            features.append(self.ghost.ghosts[ghost]["trappedTime"])
        features.append(self.pellets)
        for i in range(self.height):
            for j in range(self.width):
                features.append(self.game.board[i][j])
        features.append(self.p.lives)
        return features


    def step(self, action):
        dir_buffer = self.actions[action]
        for direction in dir_buffer:
            self.scatter = True
            self.reward -= 0.05
            if self.pellets == 0:
                    return (self.features(), self.reward + 10000, True, {})
            if self.chaseTime == 'inf' and self.scatterTime == 0:
                self.scatter = False
            elif self.scatterTime == 0 and self.chaseTime > 0:
                self.scatter = False
            elif self.chaseTime == 0:
                self.phase += 1
                self.scatterTime = self.scatterLevel[self.level][self.phase-1][0]
                self.chaseTime = self.scatterLevel[self.level][self.phase-1][1]
            #self.gameDisplay.fill(BLACK)
            self.ghosts_eaten = self.ghost.eatenHandler(self.p)
            if self.ghosts_eaten > 0:
                self.sprite_show_time = 10
                self.sprite_x, self.sprite_y = self.p.x, self.p.y
                self.sprite_value = (2**(self.ghosts_eaten + self.ghosts_combo))*100
            if self.slower == 0:
                self.ghost.move(self.p, self.game.board, self.scatter, self.frightenTimeLeft > 0)
                life = pac_life_reducer('env', self.p, self.ghost, None, self.score, self.frightenTimeLeft, self.ghosts_combo, direction, self.game, 0)
                if life == False:
                    return (self.__featureGenerator(), self.reward - 10000, True, {})
                self.slower = 2
            self.pac_next, t = self.p.move(direction, self.game.board)
            life = pac_life_reducer('env', self.p, self.ghost, None, self.score, self.frightenTimeLeft, self.ghosts_combo, direction, self.game, t)
            if life == False:
                return (self.__featureGenerator(), self.reward - 10000, True, {})
            self.frighten = True if t == 6 else False
            if t == 6:
                self.score += 50
            if t == 2:
                self.pellets -= 1
                self.score += 10
            if self.frighten:
                self.frightenTimeLeft = self.frightenTimer[self.level]
            self.slower -= 1
            if self.scatterTime > 0:
                self.scatterTime -= 1
            elif self.chaseTime != 'inf' and self.chaseTime > 0:
                self.chaseTime -= 1
            if self.frightenTimeLeft > 0:
                self.ghosts_combo += self.ghosts_eaten
                self.frightenTimeLeft -= 1
                if self.frightenTimeLeft == 0:
                    self.score += (2**self.ghosts_combo) * 100 
                    self.ghosts_combo = 0
        return (self.__featureGenerator(), self.reward, False, {})
            
    def reset(self):
        self.game = level()
        self.game.setWalls()
        self.game.setWalls()
        self.game.setFood()
        self.p = pacman()
        self.score = 0
        self.ghosts_combo = 0
        self.ghost = ghosts()
        self.count = 0
        self.pellets = sum([row.count(2) for row in self.game.board])
        self.pac = getNextSprite('right', self.count, self.pac_sprite)
        self.bsprite = self.ghost_sprite["Blinky"][self.ghost.ghosts["Blinky"]['direction']]
        self.pinksprite = self.ghost_sprite["Pinky"][self.ghost.ghosts["Pinky"]['direction']]
        self.clydesprite = self.ghost_sprite["Clyde"][self.ghost.ghosts["Clyde"]['direction']]
        self.inksprite = self.ghost_sprite["Inky"][self.ghost.ghosts["Inky"]['direction']]
        self.tick = 0  
        self.slower = 1
        self.scatter = True
        self.phase = 1
        self.level = 1
        self.frightenTimeLeft = 0
        self.sprite_show_time = 0
        self.sprite_x, self.sprite_y = 0, 0
        self.sprite_value = 0
        self.scatterTime = self.scatterLevel[self.level][self.phase-1][0]
        self.chaseTime = self.scatterLevel[self.level][self.phase-1][1]
        self.gameOver = False
        self.reward = 0
        self.gameDisplay = None
        return self.__featureGenerator()


    def render(self, mode='human', close=False):
        if close:
            pygame.quit()
        if self.gameDisplay is None:
            self.gameDisplay = pygame.display.set_mode((self.width*self.boxSize + 250, self.height*self.boxSize))
        self.gameDisplay.fill(self.BLACK)
        clock = pygame.time.Clock()
        for i in range(30):
                for j in range(28):
                    if self.game.board[i][j] == 1:
                        pygame.draw.rect(self.gameDisplay, (0, 0, 255), self.grid[i][j])
                    elif self.game.board[i][j] == 0:
                        pygame.draw.rect(self.gameDisplay, (0, 0, 0), self.grid[i][j])
                    elif self.game.board[i][j] == 7:
                        self.gameDisplay.blit(self.pac, (j*self.boxSize, i*self.boxSize))
                    elif self.game.board[i][j] == 2:
                        self.gameDisplay.blit(self.food_sprite, (j*self.boxSize, i*self.boxSize))
                    elif self.game.board[i][j] == 6:
                        self.gameDisplay.blit(self.superfood_sprite, (j*self.boxSize, i*self.boxSize))
        text = self.font.render('Score: {}'.format(self.score), True, YELLOW, BLACK)
        self.gameDisplay.blit(self.bsprite, (self.ghost.ghosts["Blinky"]['y'] * self.boxSize, self.ghost.ghosts["Blinky"]['x'] * self.boxSize))
        self.gameDisplay.blit(self.pinksprite, (self.ghost.ghosts["Pinky"]['y'] * self.boxSize, self.ghost.ghosts["Pinky"]['x'] * self.boxSize))
        self.gameDisplay.blit(self.clydesprite, (self.ghost.ghosts["Clyde"]['y'] * self.boxSize, self.ghost.ghosts["Clyde"]['x'] * self.boxSize))
        self.gameDisplay.blit(self.inksprite, (self.ghost.ghosts["Inky"]['y'] * self.boxSize, self.ghost.ghosts["Inky"]['x'] * self.boxSize))
        self.gameDisplay.blit(text, self.scoreRect)
        self.pac = getNextSprite(self.pac_next, self.count, self.pac_sprite)
        livesDisplay(self.p, self.gameDisplay, self.width, self.boxSize, self.pac_sprite[2])
        self.bsprite = self.ghost_sprite["Blinky"][self.ghost.ghosts["Blinky"]['direction']] if self.frightenTimeLeft == 0 or self.ghost.ghosts["Blinky"]['trapped'] else self.frightened_ghost
        if self.ghost.ghosts["Blinky"]["eaten"]:
            self.bsprite = self.ghost_sprite["EatenGhost"][self.ghost.ghosts["Blinky"]['direction']]
        self.pinksprite = self.ghost_sprite["Pinky"][self.ghost.ghosts["Pinky"]['direction']] if self.frightenTimeLeft == 0 or self.ghost.ghosts["Pinky"]['trapped'] else self.frightened_ghost
        if self.ghost.ghosts["Pinky"]["eaten"]:
            self.pinksprite = self.ghost_sprite["EatenGhost"][ghost.ghosts["Pinky"]['direction']]
        self.clydesprite = self.ghost_sprite["Clyde"][self.ghost.ghosts["Clyde"]['direction']] if self.frightenTimeLeft == 0 or self.ghost.ghosts["Clyde"]['trapped'] else self.frightened_ghost
        if self.ghost.ghosts["Clyde"]["eaten"]:
            self.clydesprite = self.ghost_sprite["EatenGhost"][self.ghost.ghosts["Clyde"]['direction']]
        self.inksprite = self.ghost_sprite["Inky"][self.ghost.ghosts["Inky"]['direction']] if self.frightenTimeLeft == 0 or self.ghost.ghosts["Inky"]['trapped'] else self.frightened_ghost
        if self.ghost.ghosts["Inky"]["eaten"]:
            self.inksprite = self.ghost_sprite["EatenGhost"][self.ghost.ghosts["Inky"]['direction']]
        if self.sprite_show_time > 0:
            self.gameDisplay.blit(self.scoreSprite[self.sprite_value], (self.sprite_y * self.boxSize, self.sprite_x * self.boxSize))
            self.sprite_show_time -= 1
            if self.sprite_show_time == 0:
                self.sprite_value = 0
        clock.tick(350)
        pygame.display.update()

if __name__ == '__main__':
    PacmanPygame()