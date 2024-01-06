import pygame


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, filepath, W, H):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filepath).convert_alpha()
        self.t_rect = self.image.get_rect(centerx=W // 2, bottom=H - 20)
        self.mask = pygame.mask.from_surface(self.image)
