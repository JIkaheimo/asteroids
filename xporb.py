import pygame
from circleshape import CircleShape
from constants import XP_ORB_LIFETIME


class XPOrb(CircleShape):
    def __init__(self, x, y, value):
        super().__init__(x, y, 5)
        self.value = value
        self.lifetime = XP_ORB_LIFETIME
        self.color = pygame.Color("magenta")

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
