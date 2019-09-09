import pygame
def winScreen(gameDisplay, score):
    pygame.init()
    w, h = gameDisplay.get_size()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Congratulations! No levels for now!', True, (255, 255, 0), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (w//2, h//2)
    text2 = font.render('Score: {}'.format(score), True, (255, 255, 0), (0, 0, 0))
    textRect2 = text2.get_rect()
    textRect2.center = (w//2, h//2  + 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(text, textRect)
        gameDisplay.blit(text2, textRect2)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    winScreen(pygame.display.set_mode((28*25 + 250, 30*25)), 1600)