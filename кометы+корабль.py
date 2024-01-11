import os
import sqlite3
import sys
from random import randint

import pygame

from ball import Ball
from coin2 import Coin
from ship1 import SpaceShip
from AnimatedLife import AnimatedLife

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)
BLACK = (0, 0, 0)
W, H = 1300, 770
sc = pygame.display.set_mode((W, H))
lives = 3
count_coins = 0
count_balls = 0
f = pygame.font.SysFont('arial', 30)


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

# ship = pygame.image.load('data/ship.png').convert_alpha()
# t_rect = ship.get_rect(centerx=W // 2, bottom=H - 20)
# mask = pygame.mask.from_surface(ship)
ship = SpaceShip("data\ship.png", W, H)

clock = pygame.time.Clock()
fps = 60
balls_images = ['stone4.png', 'stone5.png', 'stone3.png']
balls_surf = [load_image(path) for path in balls_images]
coins_surf = load_image('coin.png')
hearts_surf = load_image('hearts.png')
balls = pygame.sprite.Group()
coins = pygame.sprite.Group()
hearts = pygame.sprite.Group()


def get_balls():

    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()
    connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'top' (id INTEGER, Username TEXT, Balls INTEGER)")
    connection.commit()
    result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
    id1 = result_id[0][0]
    cursor.execute("INSERT INTO top VALUES (?, ?,?)", (id1 + 1, '', all_balls))

    connection.commit()
    connection.close()


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
    global lives
    global running
    for ball in balls:
        # if t_rect.collidepoint(ball.rect.center):
        # game_score += ball.score
        if ship.t_rect.collidepoint(ball.rect.center):
            # game_score += ball.score
            ball.kill()
            if lives > 1:
                lives -= 1
            else:
                get_balls()
                running = False
                # get_balls()
                all_balls = 0
                lives = 3
                count_coins = 0
                count_balls = 0
            # проигрыш


def collideCoins():
    global count_coins
    global count_balls
    global game_score
    global lives
    for coin in coins:
        # if t_rect.collidepoint(coin.rect.center):
        if ship.t_rect.collidepoint(coin.rect.center):
            # game_score += ball.score
            coin.kill()
            count_coins += 5
            count_balls += 10
            if count_coins == 1:
                count_coins = 0
                if lives < 3:
                    lives += 1


k = 0
speed = 10
running = True
while running:
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
        ship.t_rect.x -= speed
        if ship.t_rect.x < 0:
            ship.t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        ship.t_rect.x += speed
        if ship.t_rect.x > W - ship.t_rect.width:
            ship.t_rect.x = W - ship.t_rect.width

    sc.blit(bg, (0, 0))
    balls.draw(sc)
    coins.draw(sc)
    sc.blit(ship.image, ship.t_rect)
    sc.blit(load_image('notch.png'), (0, 0))
    all_balls = count_balls + k * 10

    sc_str1 = f.render(str("Баллы"), 1, (0, 0, 0))
    sc.blit(sc_str1, (20, 10))

    sc_balls = f.render(str(all_balls), 1, (0, 0, 0))
    sc.blit(sc_balls, (40, 40))

    sc_str2 = f.render(str("Жизни"), 1, (0, 0, 0))
    sc.blit(sc_str2, (120, 10))

    sc_text = f.render(str(lives), 1, (0, 0, 0))
    sc.blit(sc_text, (150, 40))

    if lives == 3:
        # sc.blit(load_image('life.png'), (0, 65))
        heart = AnimatedLife(load_image('hearts.png'), 2, 5, 0, 65, hearts)
        sc.blit(load_image('life.png'), (77, 65))
        sc.blit(load_image('life.png'), (154, 65))
    if lives == 2:
        sc.blit(load_image('life.png'), (0, 65))
        sc.blit(load_image('life.png'), (77, 65))
    else:
        sc.blit(load_image('life.png'), (0, 65))

    pygame.display.update()

    clock.tick(fps)
    balls.update(H)
    coins.update(H)
    collideBalls()
    collideCoins()
