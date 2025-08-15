import pygame
import random
from circleshape import CircleShape
from constants import POWERUP_LIFETIME


class PowerUp(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.type = random.choice(["shotgun", "triple"])
        self.lifetime = POWERUP_LIFETIME
        if self.type == "shotgun":
            self.color = pygame.Color("orange")
        else:
            self.color = pygame.Color("cyan")

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        pygame.draw.circle(
            screen, pygame.Color("white"), self.position, self.radius, 2
        )
