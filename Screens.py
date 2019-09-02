import pygame
def winScreen():
    pygame.init()
    h, w = 200, 700
    gameDisplay = pygame.display.set_mode((w, h))
    pygame.display.set_caption("You Win! This level atleast.")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Congratulations! No levels for now!', True, (0, 255, 0), (0, 0, 255))
    textRect = text.get_rect()
    textRect.center = (w//2, h//2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill((0, 0, 255))
        gameDisplay.blit(text, textRect)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    winScreen()