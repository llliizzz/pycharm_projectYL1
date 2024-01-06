import pygame

class Ball(pygame.sprite.Sprite):
<<<<<<< HEAD
    def __init__(self, x, speed, surf, score, group):
=======
    def __init__(self, x, speed, surf, group):
>>>>>>> 628dc61eef4add391bf62619db14505e3c2b9d2d
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
<<<<<<< HEAD
        self.score = score
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 60:
            self.rect.y += self.speed
        else:
            self.kill()
=======
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()
>>>>>>> 628dc61eef4add391bf62619db14505e3c2b9d2d
