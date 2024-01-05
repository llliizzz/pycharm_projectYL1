import os
import sys

import pygame
from ball import Ball
from random import randint

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

BLACK = (0, 0, 0)

W, H = 1000, 570
sc = pygame.display.set_mode((W, H))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


bg = load_image("background.jpg")

clock = pygame.time.Clock()
FPS = 60

balls_images = ['stone4.png', 'stone5.png', 'stone6.png']
balls_surf = [load_image(path) for path in balls_images]

balls = pygame.sprite.Group()


def createBall(group):
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Ball(x, speed, balls_surf[indx], group)


createBall(balls)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createBall(balls)

    sc.blit(bg, (0, 0))
    balls.draw(sc)
    pygame.display.update()

    clock.tick(FPS)

    balls.update(H)
