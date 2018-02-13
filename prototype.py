import os, pygame, random, sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.event.pump()
os.environ['SDL_VIDEO_CENTERED'] = '1'
cwd = os.path.abspath('res/')

class Image(pygame.sprite.Sprite):
    def __init__(self, imageName, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(cwd + imageName).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

background = Image("/background.png")
screen.blit(background.image, background.rect)

def render_images():
    renders.clear(screen, background.image)
    renders.draw(screen)
    pygame.display.flip()

def event_loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
                
        if pygame.key.get_focused():
            k = pygame.key.get_pressed()
            if k[pygame.K_UP]:
                car.rect.move_ip(0, -1)
            if k[pygame.K_DOWN]:
                car.rect.move_ip(0, 1)
            if k[pygame.K_LEFT]:
                car.rect.move_ip(-1, 0)
            if k[pygame.K_RIGHT]:
                car.rect.move_ip(1, 0)
    
        render_images()

car = Image("/car.png")
renders = pygame.sprite.Group(car)

event_loop()
