import os
import sys
from random import randint

import pygame

from ball import Ball
from coin2 import Coin

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
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


bg = load_image("background.jpg")

ship = pygame.image.load('data/ship.png').convert_alpha()
t_rect = ship.get_rect(centerx=W // 2, bottom=H - 20)
#mask = pygame.mask.from_surface(ship)

clock = pygame.time.Clock()
fps = 60

balls_images = ['stone4.png', 'stone5.png', 'stone6.png']
balls_surf = [load_image(path) for path in balls_images]

coins_surf = load_image('coin.png')

balls = pygame.sprite.Group()
coins = pygame.sprite.Group()


def createBall(group):
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Ball(x, speed, balls_surf[indx], group)


createBall(balls)


def createCoin(group):
    # indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Coin(x, speed, coins_surf, group)


createCoin(coins)


def collideBalls():
    global game_score
    for ball in balls:
        if t_rect.collidepoint(ball.rect.center):
            #game_score += ball.score
            ball.kill()


def collideCoins():
    global game_score
    for coin in coins:
        if t_rect.collidepoint(coin.rect.center):
            # game_score += ball.score
            coin.kill()


k = 0
speed = 10
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createBall(balls)
            k += 1
            if not (k % 5):
                createCoin(coins)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = W - t_rect.width
    elif keys[pygame.K_RIGHT]:
        t_rect.x += speed
        if t_rect.x > W - t_rect.width:
            t_rect.x = 0

    sc.blit(bg, (0, 0))
    balls.draw(sc)
    coins.draw(sc)
    sc.blit(ship, t_rect)
    pygame.display.update()

    clock.tick(fps)

    balls.update(H)
    coins.update(H)

    collideBalls()
    collideCoins()
# if __name__ == '__main__':
#     running = True
#     clock = pygame.time.Clock()
#     screen.fill((255, 255, 255))
#
#     all_sprites = pygame.sprite.Group()
#
#     drag = AnimatedCoin(load_image("pygame-8-1.png", -1), 8, 2,
#                         width - 150, height - 150,
#                         dragon, all_sprites)
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.USEREVENT:
#                 createBall(balls)
