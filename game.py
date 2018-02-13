import os, pygame, random, sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.event.pump()
start = 23
offset = 126
os.environ['SDL_VIDEO_CENTERED'] = '1'
cwd = os.path.abspath('res/')

class Image(pygame.sprite.Sprite):
    def __init__(self, imageName, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(cwd + imageName).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.angle = 90
        self.rect.x = x
        self.rect.y = y

    def rotate(self, change):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.angle = (self.angle + change) % 360
        pygame.time.delay(1)

    def moveForward(self, neg, pos):
        pygame.time.delay(5)
        if self.angle > 15 and self.angle <= 30:
            self.rect.move_ip(pos, pos*2)
        elif self.angle > 30 and self.angle <= 60:
            self.rect.move_ip(pos*2, pos*2)
        elif self.angle > 60 and self.angle <= 75:
            self.rect.move_ip(pos*2, pos)
        elif self.angle > 75 and self.angle <= 105:
            self.rect.move_ip(pos*2, 0)
        elif self.angle > 105 and self.angle <= 120:
            self.rect.move_ip(pos*2, neg)
        elif self.angle > 120 and self.angle <= 150:
            self.rect.move_ip(pos*2, neg*2)
        elif self.angle > 150 and self.angle <= 165:
            self.rect.move_ip(pos, neg*2)
        elif self.angle > 165 and self.angle <= 195:
            self.rect.move_ip(0, neg*2)
        elif self.angle > 195 and self.angle <= 210:
            self.rect.move_ip(neg, neg*2)
        elif self.angle > 210 and self.angle <= 240:
            self.rect.move_ip(neg*2, neg*2)
        elif self.angle > 240 and self.angle <= 255:
            self.rect.move_ip(neg*2, neg)
        elif self.angle > 255 and self.angle <= 285:
            self.rect.move_ip(neg*2, 0)
        elif self.angle > 285 and self.angle <= 300:
            self.rect.move_ip(neg*2, pos)
        elif self.angle > 300 and self.angle <= 330:
            self.rect.move_ip(neg*2, pos*2)
        elif self.angle > 330 and self.angle <= 345:
            self.rect.move_ip(neg, pos*2)
        elif self.angle > 345 or self.angle <= 15:
            self.rect.move_ip(0, pos*2)
    
    def check_constraints(self):
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, height)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        if parkGoal.rect.y == 0 and bottomGoal.colliderect(self):
            randomize_goal()
            update_goals()
        elif parkGoal.rect.y == 416 and topGoal.colliderect(self):
            randomize_goal()
            update_goals()

#General properties
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
rotation = 0.8

background = Image("/background.png")
screen.blit(background.image, background.rect)

#General functions
def randomize_goal():
    randX = random.randint(0, 5)
    randY = random.randint(0, 1)
    parkGoal.rect.x = start + (offset * randX)
    parkGoal.rect.y = randY * 416

def update_goals():
    renders.add(nice)
    pygame.time.set_timer(25, 900)
    topGoal.left = parkGoal.rect.left
    topGoal.top = parkGoal.rect.top + 3
    bottomGoal.left = parkGoal.rect.left
    bottomGoal.top = parkGoal.rect.bottom - 3

def rotate_car(const):
    for sprite in carGroup:
        sprite.rotate(const * rotation)

def back_up():
    beepBeep.play(0, 0, 100)

def move_car(dx, dy):
    if dx < 1:
        if reverselights in renders:
            renders.remove(reverselights)
            renders.add(taillights)
        car.moveForward(dx, dy)
    else:
        renders.remove(taillights)
        renders.add(reverselights)
        car.moveForward(dx, dy)

def render_images():
    renders.clear(screen, background.image)
    for sprite in carGroup:
        sprite.rect.clamp_ip(car.rect)
    nice.rect.clamp_ip(background.rect)
    renders.draw(screen)
    pygame.display.flip()

def event_loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == 25:
                renders.remove(nice)
                
        if pygame.key.get_focused():
            k = pygame.key.get_pressed()
            if k[pygame.K_UP]:
                move_car(-1, 1)
            if k[pygame.K_DOWN]:
                back_up()
                move_car(1, -1)
            if k[pygame.K_LEFT]:
                rotate_car(1)
            if k[pygame.K_RIGHT]:
                rotate_car(-1)
            car.check_constraints()
    
        render_images()

#Initialization (generally) 
nice = Image("/nice.png", 330, 260)
car = Image("/car.png", 20, 200)
headlights = Image("/headlights.png")
taillights = Image("/taillights.png")
reverselights = Image("/reverselights.png")
parkGoal = Image("/parkGoal.png", start)
randomize_goal()
topGoal = pygame.Rect(parkGoal.rect.left + 50, parkGoal.rect.top + 3, 20, 1)
bottomGoal = pygame.Rect(parkGoal.rect.left + 50, parkGoal.rect.bottom - 3, 20, 1)
carGroup = pygame.sprite.Group(car, headlights, taillights, reverselights)
renders = pygame.sprite.Group(parkGoal, car, headlights, taillights)
for sprite in carGroup:
    sprite.rotate(0)

beepBeep = pygame.mixer.Sound(cwd + "/beepBeep.ogg")
beepBeep.set_volume(0.1)

event_loop()
