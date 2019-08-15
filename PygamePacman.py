import pygame
from PacmanAndFriends import pacman
from Level import level
g = level()
g.setWalls()
g.setFood()
p = pacman()
direction = 'down'
pygame.init()
gameDisplay = pygame.display.set_mode((560, 600))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()
grid = []
width = 28
height = 30
boxSize = 20
food_sprite = pygame.image.load("./images/Food.png")
food_sprite = pygame.transform.scale(food_sprite, (boxSize, boxSize))
pac_sprite = [None]*3

for i in range(1,4):
    pac_sprite[i-1] = pygame.image.load("./images/Pac" + str(i) + ".png")
    pac_sprite[i-1] = pygame.transform.scale(pac_sprite[i-1], (boxSize, boxSize))

count = 0

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
while True:
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
    pac = getNextSprite(p.move(direction, g.board))
    pygame.display.flip()
    clock.tick(10)
