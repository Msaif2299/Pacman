import pygame
from pacman import pacman
from ghosts import ghosts
from Level import level
from Screens import winScreen

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

def livesDisplay(pac, gameDisplay, width, boxSize, pac_sprite):
    x_coord = width*boxSize + 50
    for x in range(pac.lives):
        gameDisplay.blit(pac_sprite, (x_coord, 200))
        x_coord += (boxSize + 20)

def newGame():
    pass

def setBack(pac, ghosts, frightenedTimeLeft, ghosts_combo, direction, game, t):
    direction = 'down'
    frightenedTimeLeft = 0
    ghosts_combo = 0
    game.board[pac.x][pac.y] = t
    t = 0
    pac.oldx = 0
    pac.oldy = 0
    pac.x = 1
    pac.y = 1
    pac.vx = 0
    pac.vy = 1
    game.board[pac.x][pac.y] = 7
    for g in ghosts.GHOSTS:
        ghosts.ghosts[g] = {}
        for var, val in zip(["x", "y", "direction", "trapped", "frightened", "eaten", "trappedTime"], [14, 11, 'right', True, False, False, 0]):
            ghosts.ghosts[g][var] = val
    ghosts.ghosts["Blinky"]['x'] = 11
    ghosts.ghosts["Blinky"]['y'] = 14
    ghosts.ghosts["Blinky"]['direction'] = 'right'
    ghosts.ghosts["Blinky"]['trapped'] = False
    ghosts.ghosts["Pinky"]['x'], ghosts.ghosts["Pinky"]['y'], ghosts.ghosts["Pinky"]['direction'], ghosts.ghosts["Pinky"]['trapped'] = 14, 16, 'left', True
    for g, time in zip(["Blinky", "Inky", "Pinky", "Clyde"], [i*50 for i in range(4)]):
            ghosts.ghosts[g]['trappedTime'] = time

def pac_life_reducer(pac, ghosts, gameDisplay, score, frightenedTimeLeft, ghosts_combo, direction, game, t):
    w, h = pygame.display.get_surface().get_size()
    for g in ghosts.GHOSTS:
        if pac.x == ghosts.ghosts[g]['x'] and pac.y == ghosts.ghosts[g]['y'] and not ghosts.ghosts[g]['frightened'] and not ghosts.ghosts[g]['eaten']:
            pac.lives -= 1
            if pac.lives < 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN: 
                                gameDisplay.fill((255, 0, 0))
                    gameDisplay.fill(BLACK)
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    text = font.render('Game Over', True, YELLOW, BLACK)
                    text_rect = text.get_rect()
                    text_rect.center = (w//2, h//2)
                    gameDisplay.blit(text, text_rect)
                    text = font.render('Score: {}'.format(score), True, YELLOW, BLACK)
                    text_rect = text.get_rect()
                    text_rect.center = (w//2, h//2 + 75)
                    gameDisplay.blit(text, text_rect)
                    pygame.display.flip()
            else:
                setBack(pac, ghosts, frightenedTimeLeft, ghosts_combo, direction, game, t)
                return

g = level()
g.setWalls()
g.setFood()
p = pacman()
direction = 'down'
pygame.init()
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
boxSize = 25
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Score: 0', True, YELLOW, BLACK)
scoreSprite = {}
for score in [(2**i)*100 for i in range(1, 5)]:
    scoreSprite[score] = pygame.transform.scale(pygame.image.load('./images/{}.png'.format(score)), (boxSize, boxSize))
scoreRect = text.get_rect()
width = 28
height = 30
score = 0
ghosts_combo = 0
gameDisplay = pygame.display.set_mode((width*boxSize + 250, height*boxSize))
scoreRect.center = (width*boxSize + 100, 50)
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

def printAll(ghosts, pac):
    for g in ghosts.GHOSTS:
        print('{}: (x: {}, y: {}')
    print('Pac: (x: {}, y: {}')

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
frightenTimer = {1: 40, 2: 20}
frightenTimeLeft = 0
sprite_show_time = 0
sprite_x, sprite_y = 0, 0
sprite_value = 0
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
    gameDisplay.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: direction = 'left'
            if event.key == pygame.K_RIGHT: direction = 'right'
            if event.key == pygame.K_UP: direction = 'up'
            if event.key == pygame.K_DOWN: direction = 'down'
    ghosts_eaten = ghost.eatenHandler(p)
    if ghosts_eaten > 0:
        sprite_show_time = 10
        sprite_x, sprite_y = p.x, p.y
        sprite_value = (2**(ghosts_eaten + ghosts_combo))*100
    if slower == 0:
        ghost.move(p, g.board, scatter, frightenTimeLeft > 0)
        pac_life_reducer(p, ghost, gameDisplay, score, frightenTimeLeft, ghosts_combo, direction, g, 0)
        slower = 2
    pac_next, t = p.move(direction, g.board)
    pac_life_reducer(p, ghost, gameDisplay, score, frightenTimeLeft, ghosts_combo, direction, g, t)
    frighten = True if t == 6 else False
    if t == 6:
        score += 50
    if t == 2:
        pellets -= 1
        score += 10
    if frighten:
        frightenTimeLeft = frightenTimer[level]
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
    text = font.render('Score: {}'.format(score), True, YELLOW, BLACK)
    gameDisplay.blit(bsprite, (ghost.ghosts["Blinky"]['y'] * boxSize, ghost.ghosts["Blinky"]['x'] * boxSize))
    gameDisplay.blit(pinksprite, (ghost.ghosts["Pinky"]['y'] * boxSize, ghost.ghosts["Pinky"]['x'] * boxSize))
    gameDisplay.blit(clydesprite, (ghost.ghosts["Clyde"]['y'] * boxSize, ghost.ghosts["Clyde"]['x'] * boxSize))
    gameDisplay.blit(inksprite, (ghost.ghosts["Inky"]['y'] * boxSize, ghost.ghosts["Inky"]['x'] * boxSize))
    gameDisplay.blit(text, scoreRect)
    pac = getNextSprite(pac_next)
    livesDisplay(p, gameDisplay, width, boxSize, pac_sprite[2])
    bsprite = ghost_sprite["Blinky"][ghost.ghosts["Blinky"]['direction']] if frightenTimeLeft == 0 or ghost.ghosts["Blinky"]['trapped'] else frightened_ghost
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
    if sprite_show_time > 0:
        gameDisplay.blit(scoreSprite[sprite_value], (sprite_y * boxSize, sprite_x * boxSize))
        sprite_show_time -= 1
        if sprite_show_time == 0:
            sprite_value = 0
    pygame.display.flip()
    clock.tick(10)
    slower -= 1
    if scatterTime > 0:
        scatterTime -= 1
    elif chaseTime != 'inf' and chaseTime > 0:
        chaseTime -= 1
    if frightenTimeLeft > 0:
        ghosts_combo += ghosts_eaten
        frightenTimeLeft -= 1
        if frightenTimeLeft == 0:
            score += (2**ghosts_combo) * 100 
            ghosts_combo = 0
            
if gameOver == False:
    winScreen(gameDisplay, score)