import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x,group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        # self.rect = self.image.get_rect(center=(x, 0))
        # self.speed = speed
        self.add(group)