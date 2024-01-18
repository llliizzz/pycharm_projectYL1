import os
import random
import sqlite3
import sys
from random import randint
import pygame
from ball import Ball
from coin2 import Coin
from ship1 import SpaceShip
from AnimatedLife import AnimatedLife

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
    # else:
    #     image = image.convert_alpha()
    return image


def pause(sc, W, H):
    font = pygame.font.SysFont(None, 40)
    WHITE = (255, 255, 255)
    paused_text = font.render('Paused. Press SPACE to resume.', True, WHITE)
    paused_rect = paused_text.get_rect(center=(W // 2, H // 2))
    transparent = pygame.Surface((W, H))
    transparent.set_alpha(10)

    for i in range(3):
        sc.blit(transparent, (0, 0))
        sc.blit(paused_text, paused_rect)
        pygame.display.flip()
        pygame.time.wait(30)


def get_balls(all_balls):
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


def createBall(group, balls_surf, W):
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)
    return Ball(x, speed, balls_surf[indx], group)


def createCoin(group, coins_surf, W):
    # indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)
    return Coin(x, speed, coins_surf, group)


def collideBalls(balls, ship, boom_sound):
    global game_score
    global count_coins
    global count_balls
    global lives
    global running
    global all_balls
    for ball in balls:
        if ship.t_rect.collidepoint(ball.rect.center):
            boom_sound.play()
            ball.kill()
            Particle.create_particles(ball.rect.center)
            if lives > 1:
                lives -= 1
            else:
                get_balls(all_balls)
                running = False
                all_balls = 0
                lives = 3
                count_coins = 0
                count_balls = 0
                from FINAL_3 import finalScreen
                finalScreen()
            # проигрыш


def collideCoins(coins, ship, coin_sound):
    global count_coins
    global count_balls
    global game_score
    global lives
    for coin in coins:
        if ship.t_rect.collidepoint(coin.rect.center):
            # game_score += ball.score
            coin_sound.play()
            coin.kill()
            count_coins += 5
            count_balls += 10
            if count_coins == 1:
                count_coins = 0
                if lives < 3:
                    lives += 1



class Particle(pygame.sprite.Sprite):
    global sprites_sprites
    fire = [load_image("star.png")]
    # fire  = pygame.image.load('data/star.png').convert_alpha()
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, group, W, H):
        super().__init__(group)
        global sprites_sprites
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

        self.screen_rect = (0, 0, W, H)

    def update(self):
        global screen_rect
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.screen_rect):
            self.kill()

    def create_particles(position):
        numbers = range(-50, 50)
        for _ in range(20):
            Particle(position, random.choice(numbers), random.choice(numbers),  sprites_sprites, 1300, 770)


def game():
    global count_coins
    global count_balls
    global sprites_sprites
    global lives
    global all_balls
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    BLACK = (0, 0, 0)
    W, H = 1300, 770
    sc = pygame.display.set_mode((W, H))
    x = 10
    y = 10
    os.environ['Sp_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    lives = 3
    count_coins = 0
    count_balls = 0
    f = pygame.font.SysFont('arial', 30)
    boom_sound = pygame.mixer.Sound('audio/boom_sound.wav')
    coin_sound = pygame.mixer.Sound('audio/coin_sound.wav')
    paused = False
    bg = load_image("background.jpg")
    ship = SpaceShip("data/ship.png", W, H)
    clock = pygame.time.Clock()
    fps = 60
    balls_images = ['stone4.png', 'stone5.png', 'stone3.png']
    balls_surf = [load_image(path) for path in balls_images]
    coins_surf = load_image('coin.png')
    balls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    createBall(balls, balls_surf, 1300)
    createCoin(coins, coins_surf, 1300)
    k = 0
    speed = 10
    running = True
    all_sprites = pygame.sprite.Group()
    sprites_sprites = pygame.sprite.Group()

    heart1 = AnimatedLife(load_image('heart1.png'), 5, 2, 10, 70, all_sprites)
    heart2 = AnimatedLife(load_image('heart1.png'), 5, 2, 70, 70, all_sprites)
    heart3 = AnimatedLife(load_image('heart1.png'), 5, 2, 130, 70, all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT:
                if not paused:
                    createBall(balls, balls_surf, 1300)
                    k += 1
                    if not (k % 5):
                        createCoin(coins, coins_surf, 1300)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:
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

            if lives == 2:
                heart3.kill()
            elif lives == 1:
                heart2.kill()

            all_sprites.draw(sc)
            all_sprites.update()
            pygame.display.update()
            clock.tick(fps)
            balls.update(H)
            coins.update(H)
            collideBalls(balls, ship, boom_sound)
            collideCoins(coins, ship, coin_sound)
        else:
            pause(sc, 0, 0)

game()