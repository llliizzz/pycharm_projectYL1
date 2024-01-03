import os
import random
import sys

import pygame

pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)
# global k
k = 0


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


class Ball(pygame.sprite.Sprite):
    image = load_image("stone3.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        # self.radius = radius
        # self.image = pygame.Surface((2 * radius, 2 * radius),
        #                             pygame.SRCALPHA, 32)
        # pygame.draw.circle(self.image, pygame.Color("red"),
        #                    (radius, radius), radius)
        x = random.randrange(width)
        y = 0
        self.rect = pygame.Rect(x, y, x + 110, y + 110)
        self.vx = 0
        self.vy = random.randrange(1, 5)
        # self.vy = 5

    def update(self):
        global k
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            k += 1
        # if pygame.sprite.spritecollideany(self, vertical_borders):
        #      del pygame.sprite


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([max(x2 - x1, 1), max(y2 - y1, 1)])
        self.rect = pygame.Rect(x1, y1, max(x2 - x1, 1), max(y2 - y1, 1))


class MovingSquare(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.color = 0
        self.pos = [10, 10]
        self.dx, self.dy = 0, 0
        self.image = pygame.Surface([])
        screen.fill((self.color, self.color, self.color), (*self.pos, 50, 50))

    # def process_event(self, event):
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_RIGHT:
    #             self.dx = 10
    #         elif event.key == pygame.K_LEFT:
    #             self.dx = -10
    #         elif event.key == pygame.K_UP:
    #             self.dy = -10
    #         elif event.key == pygame.K_DOWN:
    #             self.dy = 10
    #     elif event.type == pygame.KEYUP:
    #         if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
    #             self.dx = 0
    #         elif event.key in (pygame.K_UP, pygame.K_DOWN):
    #             self.dy = 0

    def move(self):
        self.color = (self.color + 1) % 256
        # self.pos[0] += self.dx
        # self.pos[1] += self.dy
        self.pos[0] = self.pos[0]
        self.pos[1] += 10


n = 0
if __name__ == '__main__':
    running = True
    fps = 30
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    Border(5, 5, width - 5, 5, horizontal_borders, all_sprites)
    Border(5, height - 5, width - 5, height - 5, horizontal_borders, all_sprites)
    Border(5, 5, 5, height - 5, vertical_borders, all_sprites)
    Border(width - 5, 5, width - 5, height - 5, vertical_borders, all_sprites)
    for i in range(10):
        Ball(balls, all_sprites)
    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    while running:
        n += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # screen.fill((255, 255, 255),
        #             (0, 0, width, height))
        balls.update()
        vertical_borders.draw(screen)
        horizontal_borders.draw(screen)
        balls.draw(screen)
        # if (n * 10 - k) > 5:
        #     balls.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    print(n)
