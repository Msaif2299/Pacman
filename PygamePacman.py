import pygame
from PacmanAndFriends import pacman, ghosts
from Level import level
from Screens import winScreen
g = level()
g.setWalls()
g.setFood()
p = pacman()
direction = 'down'
pygame.init()
width = 28
height = 30
boxSize = 25
score = 0
gameDisplay = pygame.display.set_mode((width*boxSize, height*boxSize))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()
grid = []
food_sprite = pygame.image.load("./images/Food.png")
food_sprite = pygame.transform.scale(food_sprite, (boxSize, boxSize))
superfood_sprite = pygame.transform.scale(pygame.image.load("./images/SuperFood.png"), (boxSize, boxSize))
pac_sprite = [None]*3
ghost_sprite = {}
GHOST_NAMES = ["Blinky", "Pinky", "Inky", "Clyde", "EatenGhost"]
CARDINAL_DIRECTIONS = ["Up", "Down", "Left", "Right"]
for gh in GHOST_NAMES:
    ghost_sprite[gh] = {}
for gh in ghost_sprite.keys():
    for direction in CARDINAL_DIRECTIONS:
        ghost_sprite[gh][direction.lower()] = pygame.transform.scale(pygame.image.load("./images/" + gh + direction + ".png"), (boxSize, boxSize))
for i in range(1,4):
    pac_sprite[i-1] = pygame.image.load("./images/Pac" + str(i) + ".png")
    pac_sprite[i-1] = pygame.transform.scale(pac_sprite[i-1], (boxSize, boxSize))
frightened_ghost = pygame.transform.scale(pygame.image.load("./images/Scared.png"), (boxSize, boxSize))
ghost = ghosts()
count = 0
pellets = sum([row.count(2) for row in g.board])
def getNextSprite(direction):
    global count
    angle = 0
    prev_count = count
    count += 1
    if count == 3:
        count = 0
    if direction == 'right':
        angle = 0
    elif direction == 'left':
        angle = 180
    elif direction == 'up':
        angle = 90
    elif direction == 'down':
        angle = 270
    return pygame.transform.rotate(pac_sprite[prev_count], angle)
    

for i in range(height):
    temp = []
    for j in range(width):
        temp.append(pygame.Rect(j*boxSize, i*boxSize, boxSize, boxSize))
    grid.append(temp)
pac = getNextSprite('right')
ghost.move(p, g.board)
bsprite = ghost_sprite["Blinky"][ghost.ghosts["Blinky"]['direction']]
pinksprite = ghost_sprite["Pinky"][ghost.ghosts["Pinky"]['direction']]
clydesprite = ghost_sprite["Clyde"][ghost.ghosts["Clyde"]['direction']]
inksprite = ghost_sprite["Inky"][ghost.ghosts["Inky"]['direction']]
tick = 0  
slower = 1
scatter = True
phase = 1
level = 1
scatterLevel = {1: [[14, 40], [14, 40], [10, 40], [10, 'inf']], 
                2: [[14, 40], [14, 40], [10, 1033], [10, 'inf']]}
frightenTimer = {1: 20, 2: 20}
frightenTimeLeft = 0
scatterTime = scatterLevel[level][phase-1][0]
chaseTime = scatterLevel[level][phase-1][1]
gameOver = False
while True:
    scatter = True
    if pellets == 0:
        gameOver = False
        break
    if chaseTime == 'inf' and scatterTime == 0:
        scatter = False
    elif scatterTime == 0 and chaseTime > 0:
        scatter = False
    elif chaseTime == 0:
        phase += 1
        scatterTime = scatterLevel[level][phase-1][0]
        chaseTime = scatterLevel[level][phase-1][1]
    gameDisplay.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: direction = 'left'
            if event.key == pygame.K_RIGHT: direction = 'right'
            if event.key == pygame.K_UP: direction = 'up'
            if event.key == pygame.K_DOWN: direction = 'down'
    for i in range(30):
        for j in range(28):
            if g.board[i][j] == 1:
                pygame.draw.rect(gameDisplay, (0, 0, 255), grid[i][j])
            elif g.board[i][j] == 0:
                pygame.draw.rect(gameDisplay, (0, 0, 0), grid[i][j])
            elif g.board[i][j] == 7:
                gameDisplay.blit(pac, (j*boxSize, i*boxSize))
            elif g.board[i][j] == 2:
                gameDisplay.blit(food_sprite, (j*boxSize, i*boxSize))
            elif g.board[i][j] == 6:
                gameDisplay.blit(superfood_sprite, (j*boxSize, i*boxSize))
    gameDisplay.blit(bsprite, (ghost.ghosts["Blinky"]['y'] * boxSize, ghost.ghosts["Blinky"]['x'] * boxSize))
    gameDisplay.blit(pinksprite, (ghost.ghosts["Pinky"]['y'] * boxSize, ghost.ghosts["Pinky"]['x'] * boxSize))
    gameDisplay.blit(clydesprite, (ghost.ghosts["Clyde"]['y'] * boxSize, ghost.ghosts["Clyde"]['x'] * boxSize))
    gameDisplay.blit(inksprite, (ghost.ghosts["Inky"]['y'] * boxSize, ghost.ghosts["Inky"]['x'] * boxSize))
    pac_next, t = p.move(direction, g.board)
    frighten = True if t == 6 else False
    if t == 2:
        pellets -= 1
    if frighten:
        frightenTimeLeft = frightenTimer[level]
    pac = getNextSprite(pac_next)
    if slower == 0:
        ghost.move(p, g.board, scatter, frightenTimeLeft > 0)
        slower = 2
    bsprite = ghost_sprite["Blinky"][ghost.ghosts["Blinky"]['direction']] if frightenTimeLeft == 0 or ghost.ghosts["Blinky"]['trapped'] else frightened_ghost
    print("{}, {}".format(ghost.ghosts["Blinky"]["x"], ghost.ghosts["Blinky"]["y"]))
    if ghost.ghosts["Blinky"]["eaten"]:
        bsprite = ghost_sprite["EatenGhost"][ghost.ghosts["Blinky"]['direction']]
    pinksprite = ghost_sprite["Pinky"][ghost.ghosts["Pinky"]['direction']] if frightenTimeLeft == 0 or ghost.ghosts["Pinky"]['trapped'] else frightened_ghost
    if ghost.ghosts["Pinky"]["eaten"]:
        pinksprite = ghost_sprite["EatenGhost"][ghost.ghosts["Pinky"]['direction']]
    clydesprite = ghost_sprite["Clyde"][ghost.ghosts["Clyde"]['direction']] if frightenTimeLeft == 0 or ghost.ghosts["Clyde"]['trapped'] else frightened_ghost
    if ghost.ghosts["Clyde"]["eaten"]:
        clydesprite = ghost_sprite["EatenGhost"][ghost.ghosts["Clyde"]['direction']]
    inksprite = ghost_sprite["Inky"][ghost.ghosts["Inky"]['direction']] if frightenTimeLeft == 0 or ghost.ghosts["Inky"]['trapped'] else frightened_ghost
    if ghost.ghosts["Inky"]["eaten"]:
        inksprite = ghost_sprite["EatenGhost"][ghost.ghosts["Inky"]['direction']]
    pygame.display.flip()
    if tick < 150:
        tick += 1
    if tick == 50:
        ghost.ghosts["Pinky"]['trapped'] = False
        ghost.setFree('pinky')
    if tick == 100:
        ghost.ghosts["Inky"]['trapped'] = False
        ghost.setFree('inky')
    if tick == 150:
        tick = 151
        ghost.ghosts["Clyde"]['trapped'] = False
        ghost.setFree('clyde')
    clock.tick(10)
    slower -= 1
    if scatterTime > 0:
        scatterTime -= 1
    elif chaseTime != 'inf' and chaseTime > 0:
        chaseTime -= 1
    if frightenTimeLeft > 0:
        frightenTimeLeft -= 1
pygame.quit()
if gameOver == False:
    winScreen()